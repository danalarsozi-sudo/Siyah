import asyncio
import logging
import random
import sqlite3
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# Logging
logging.basicConfig(level=logging.INFO)

# Bot ayarları
TOKEN = "8131658723:AAGgWDY75CuZvk88EHDemJzEBKhIW77m3ZY"
ADMIN_ID = 1748533804

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Veritabanı
DB_FILE = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, lang TEXT DEFAULT 'tk', approved INTEGER DEFAULT 0, pending INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS happ_codes (code TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS imo_proxies (proxy TEXT UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

# Başlangıç Happ kodları
initial_happ = [
    "happ://crypt4/qswaa90qazYU31Tc3WLKPY9yi0fu35NkLr7HYYekD9fQOoklBW0ODu/y6zequYgjQ7bOnl8Q/QXskIeNa9dCVK65W3LcVkUI2GMS5TAmMI5uy/jQ32GH53lBiJ5qiT6j0HWK35xhxGExBr6TzFUj01jOQ453T/2b6zIU1jJ1IcnXHfgDGpYFU4i9BeBbsmqhdTm78R62O/9SdPazOtdNEvvv3FZ8Gh6pVUQSWcbTGTmK04NHs3lBWlUDWtJ5h5aCkQUV0xeO7TIb+TKl481rg0ovmyW1IiNVpZVdJUpG7tycY0tQc+U/Mn5on8bTCSpqm36cf+LoDbEvENnG1lspAX8Elv52Zx4plblBPcEDvrAyMS+HBB8aJMeE9mb3ZliCrodxVzVAvwcSAPACKlm1W6ce+ebDngpSazUULCaCsME9PwzKz+stW8Xjz8plulYGPqCg9G3cH9I5xZeqElf0wpUmaByPIeF7X39FHFLHFWFwC927Wsp1rWe7Iv+3a3kl0Mb598afCwVCT5/Jdh22bQXQSAKILNHf0n4yJexJQU8ldENBjPDq4e5bJklSOHuVT+gArYi0wFYzhtLZlFs4lIOU/mjzV2zN6VL23nMVShrpUZHzaGNB/WRuLAtpZ4VQxjMlmd4VDFUtaQoDWllxJs6WHRtT1/RxO/F2vvX2BF8="
]

initial_proxies = [
    "IP: 50.210.166.34 Port: 80 Ülke: United States Anonymity: High (HIA)",
    "IP: 209.135.168.41 Port: 80 Ülke: United States Anonymity: Anonymous",
    "IP: 146.19.254.101 Port: 5555 Ülke: Netherlands Anonymity: High",
]

def add_initial_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for code in initial_happ:
        try: c.execute("INSERT OR IGNORE INTO happ_codes (code) VALUES (?)", (code,))
        except: pass
    for proxy in initial_proxies:
        try: c.execute("INSERT OR IGNORE INTO imo_proxies (proxy) VALUES (?)", (proxy,))
        except: pass
    conn.commit()
    conn.close()

add_initial_data()

# Dil desteği
LANGUAGES = {
    'tk': {
        'welcome': "Salam! Happ VPN we IMO proxy botyna hoş geldiňiz!",
        'wait_approval': "Admin tarapyndan tassyklamaga garaşyň (@Eminvb bilen habarlaşyň)",
        'main_menu': "Saýlaň:",
        'get_happ': "Happ VPN kod almak",
        'get_imo': "IMO proxy almak",
        'how_happ': "Happ nähili ulanylýar",
        'how_imo': "IMO proxy nähili goşulýar",
        'change_lang': "Dil üýtgetmek / Изменить язык",
        'refresh': "Ýene täzele",
        'admin_panel': "Admin panel",
        'users_count': "Jemi ulanyjylar: {}",
        'pending_users': "Garaşýan ulanyjylar:",
        'approved_users': "Tassyklanan ulanyjylar:",
        'approve_btn': "Onayla",
        'add_vpn': "Täze Happ kod goş",
        'add_proxy': "Täze IMO proxy goş",
        'approved_msg': "Siziň islegiňiz tassyklandy! Botdan peýdalanyp bilersiňiz.",
        'new_user_notify': "Täze ulanyjy start basdy: @{} (ID: {})",
        'no_codes': "Häzir happ kody ýok, admin goşsun ýa-da ýene synanyşyň.",
        'no_proxies': "Häzir proxy ýok, täze goşulýar...",
    },
    'ru': {
        'welcome': "Привет! Добро пожаловать в бот Happ VPN и IMO proxy!",
        'wait_approval': "Ожидайте подтверждения от админа (@Eminvb)",
        'main_menu': "Выберите:",
        'get_happ': "Получить код Happ VPN",
        'get_imo': "Получить прокси для IMO",
        'how_happ': "Как использовать Happ",
        'how_imo': "Как добавить прокси в IMO",
        'change_lang': "Dil üýtgetmek / Изменить язык",
        'refresh': "Обновить",
        'admin_panel': "Панель админа",
        'users_count': "Всего пользователей: {}",
        'pending_users': "Ожидающие:",
        'approved_users': "Одобренные:",
        'approve_btn': "Одобрить",
        'add_vpn': "Добавить Happ код",
        'add_proxy': "Добавить IMO proxy",
        'approved_msg': "Ваша заявка одобрена! Можете использовать бота.",
        'new_user_notify': "Новый пользователь запустил: @{} (ID: {})",
        'no_codes': "Пока нет Happ кодов, админ добавит или попробуйте позже.",
        'no_proxies': "Пока нет прокси, новые добавляются...",
    }
}

def get_text(user_id, key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    lang = res[0] if res else 'tk'
    conn.close()
    return LANGUAGES.get(lang, LANGUAGES['tk']).get(key, key)

# Proxy otomatik güncelleme
async def update_proxies():
    try:
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
        ]
        new_proxies = []
        for url in urls:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                for line in resp.text.strip().splitlines():
                    if ':' in line and not line.startswith('#'):
                        ip, port = line.strip().split(':', 1)
                        new_proxies.append(f"IP: {ip} Port: {port} Ülke: Unknown Anonymity: Unknown")

        if new_proxies:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            for p in new_proxies[:50]:
                try: c.execute("INSERT OR IGNORE INTO imo_proxies (proxy) VALUES (?)", (p,))
                except: pass
            conn.commit()
            conn.close()
            logging.info(f"{len(new_proxies)} proxy denendi, yenileri eklendi.")
    except Exception as e:
        logging.error(f"Proxy update error: {e}")

# Keep-alive server
async def handle(_):
    return web.Response(text="Bot alive!")

app = web.Application()
app.router.add_get('/', handle)

async def start_keepalive():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    logging.info(f"Keep-alive server {os.getenv('PORT', 8080)} portta başladı")

# FSM
class AdminAdd(StatesGroup):
    waiting_vpn = State()
    waiting_proxy = State()

# Ana menü
def main_menu(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    lang = res[0] if res else 'tk'
    conn.close()

    keys = LANGUAGES[lang]
    buttons = [
        [InlineKeyboardButton(keys['get_happ'], callback_data="get_happ")],
        [InlineKeyboardButton(keys['get_imo'], callback_data="get_imo")],
        [InlineKeyboardButton(keys['how_happ'], callback_data="how_happ")],
        [InlineKeyboardButton(keys['how_imo'], callback_data="how_imo")],
        [InlineKeyboardButton(keys['change_lang'], callback_data="change_lang")],
    ]
    if user_id == ADMIN_ID:
        buttons.append([InlineKeyboardButton(keys['admin_panel'], callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Start komutu
@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT approved, pending FROM users WHERE user_id = ?", (user_id,))
    res = c.fetchone()

    if res:
        approved, pending = res
        if approved:
            await message.answer(get_text(user_id, 'welcome'), reply_markup=main_menu(user_id))
        elif pending:
            await message.answer(get_text(user_id, 'wait_approval'))
    else:
        c.execute("INSERT INTO users (user_id, username, pending) VALUES (?, ?, 1)", (user_id, username))
        conn.commit()
        await message.answer(get_text(user_id, 'wait_approval'))
        await bot.send_message(ADMIN_ID, get_text(ADMIN_ID, 'new_user_notify').format(username, user_id))

    conn.close()

# Callback handler (öncekiyle aynı, uzun olduğu için kısaltmadım, tam hali yukarıdaki mesajlarda var)
# ... (callback, add_vpn, add_proxy fonksiyonlarını önceki mesajdaki tam haliyle kullan, buraya tekrar yazmıyorum yer kaplamasın)

# Scheduler'ı global oluştur
scheduler = AsyncIOScheduler()
scheduler.add_job(update_proxies, 'interval', minutes=30)

# Ana fonksiyon – scheduler burada başlıyor
async def main():
    # Keep-alive başlat
    asyncio.create_task(start_keepalive())

    # Scheduler'ı event loop başladıktan sonra başlat
    scheduler.start()

    # Botu çalıştır
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
