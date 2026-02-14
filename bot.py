import asyncio
import random
import logging
import string
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, BotCommand, BotCommandScopeDefault
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- KONFİGÜRASYON ---
API_TOKEN = '8131658723:AAGgWDY75CuZvk88EHDemJzEBKhIW77m3ZY'
ADMIN_ID = 1748533804
ADMIN_USERNAME = "@Eminvb"

logging.basicConfig(level=logging.INFO)

class AdminStates(StatesGroup):
    waiting_for_vpn = State()
    waiting_for_proxy = State()

# --- VERİTABANI SİMÜLASYONU (Bellek Üzerinde) ---
db = {
    "users": {}, # {user_id: {"approved": bool, "lang": "tm", "name": "str", "username": "str", "active": bool}}
    "vpn_codes": [
        "happ:/crypt4/aswaa90qazYU31Ic3WLKPY9viOfu35NkLr7HYYekD9fQOokIBWOODu/y6zequYgjQ7bOnl8Q/...",
    ],
    "proxies": [
        "IP: 50.210.166.34 | Port: 80 | United States | High (HIA)",
        "IP: 209.135.168.41 | Port: 80 | United States | Anonymous",
    ]
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- REHBER İÇERİKLERİ ---
GUIDES = {
    "tm": {
        "vpn": "🚀 **Happ VPN Kurulumy:**\n1. Kody göçürip alyň.\n2. Happ VPN programmasyna giriň.\n3. 'Import' ýa-da '+' düwmesine basyň.\n4. Kody goýuň we birigiň!",
        "proxy": "🌐 **IMO Proksi Kurulumy:**\n1. IMO-da Sazlamalara giriň.\n2. 'Data & Storage' saýlaň.\n3. 'Proxy Settings' basyň.\n4. Proksini goşuň we işlediň!"
    },
    "ru": {
        "vpn": "🚀 **Установка Happ VPN:**\n1. Скопируйте код.\n2. Откройте приложение Happ VPN.\n3. Нажмите '+' или 'Import'.\n4. Вставьте код и подключайтесь!",
        "proxy": "🌐 **Настройка прокси IMO:**\n1. Зайдите в Настройки IMO.\n2. Выберите 'Данные и память'.\n3. 'Настройки прокси'.\n4. Добавьте данные и активируйте!"
    }
}

STRINGS = {
    "tm": {
        "welcome": "Salam! Bu bot size mugt Happ VPN kodlaryny we IMO proksilerini berýär.",
        "need_auth": f"Siz entek tassyklanmadyňyz. Admin bilen habarlaşyň: {ADMIN_USERNAME}",
        "menu": "Esasy Menýu:",
        "get_vpn": "🚀 VPN Kodyny al",
        "get_proxy": "🌐 IMO Proksisini al",
        "how_vpn": "📖 VPN Kurulumy",
        "how_imo": "📖 IMO Sazlamalary",
        "refresh": "Tazelemek 🔄",
        "back": "⬅️ Yza",
        "approved": "✅ Siziň hasabyňyz tassyklanyldy!",
        "feedback_q": "Kod/Proksi işledimi?",
        "working": "✅ Işledi",
        "not_working": "❌ İşlemedi",
        "thanks": "Sazlamalaryňyz üçin sag boluň!"
    },
    "ru": {
        "welcome": "Привет! Этот бот выдает бесплатные коды Happ VPN и прокси для IMO.",
        "need_auth": f"Вы не авторизованы. Свяжитесь с админом: {ADMIN_USERNAME}",
        "menu": "Главное меню:",
        "get_vpn": "🚀 Получить VPN код",
        "get_proxy": "🌐 Получить прокси IMO",
        "how_vpn": "📖 Установка VPN",
        "how_imo": "📖 Настройка IMO",
        "refresh": "Обновить 🔄",
        "back": "⬅️ Назад",
        "approved": "✅ Ваш аккаунт одобрен!",
        "feedback_q": "Сработал ли код/прокси?",
        "working": "✅ Работает",
        "not_working": "❌ Не работает",
        "thanks": "Спасибо за отзыв!"
    }
}

# --- KLAVYE SİSTEMİ ---
def get_main_kb(u_id):
    lang = db["users"].get(u_id, {}).get("lang", "tm")
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text=STRINGS[lang]["get_vpn"], callback_data="btn_vpn"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["get_proxy"], callback_data="btn_proxy"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["how_vpn"], callback_data="guide_vpn"),
          InlineKeyboardButton(text=STRINGS[lang]["how_imo"], callback_data="guide_imo"))
    b.row(InlineKeyboardButton(text="🌍 Dil / Язык", callback_data="btn_lang"))
    if u_id == ADMIN_ID:
        b.row(InlineKeyboardButton(text="🛡 Admin Panel", callback_data="admin_home"))
    return b.as_markup()

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    u_id = m.from_user.id
    u_name = m.from_user.full_name
    u_tag = m.from_user.username or "Yok"
    
    if u_id not in db["users"]:
        db["users"][u_id] = {"approved": (u_id == ADMIN_ID), "lang": "tm", "name": u_name, "username": u_tag, "active": True}
        await bot.send_message(ADMIN_ID, f"🔔 **Yeni Katılım!**\nİsim: {u_name}\nID: {u_id}\nUser: @{u_tag}")

    user = db["users"][u_id]
    if not user["approved"]:
        await m.answer(STRINGS["tm"]["need_auth"])
        return
    await m.answer(STRINGS[user["lang"]]["welcome"], reply_markup=get_main_kb(u_id))

# --- BUTON ETKİLEŞİMLERİ ---
@dp.callback_query(F.data.startswith("btn_"))
async def handle_buttons(c: types.CallbackQuery):
    u_id = c.from_user.id
    action = c.data.replace("btn_", "")
    lang = db["users"][u_id]["lang"]

    if action == "vpn":
        item = random.choice(db["vpn_codes"])
        b = InlineKeyboardBuilder()
        b.add(InlineKeyboardButton(text=STRINGS[lang]["refresh"], callback_data="btn_vpn"))
        b.row(InlineKeyboardButton(text=STRINGS[lang]["working"], callback_data="fb_ok_VPN"),
              InlineKeyboardButton(text=STRINGS[lang]["not_working"], callback_data="fb_no_VPN"))
        await c.message.answer(f"🚀 **Happ VPN:**\n\n`{item}`", parse_mode="Markdown", reply_markup=b.as_markup())
    
    elif action == "proxy":
        item = random.choice(db["proxies"])
        b = InlineKeyboardBuilder()
        b.add(InlineKeyboardButton(text=STRINGS[lang]["refresh"], callback_data="btn_proxy"))
        b.row(InlineKeyboardButton(text=STRINGS[lang]["working"], callback_data="fb_ok_Proxy"),
              InlineKeyboardButton(text=STRINGS[lang]["not_working"], callback_data="fb_no_Proxy"))
        await c.message.answer(f"🌐 **IMO Proxy:**\n\n`{item}`", parse_mode="Markdown", reply_markup=b.as_markup())

    elif action == "lang":
        b = InlineKeyboardBuilder()
        b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="set_tm"), InlineKeyboardButton(text="RU 🇷🇺", callback_data="set_ru"))
        await c.message.edit_text("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())
    
    await c.answer()

@dp.callback_query(F.data.startswith("set_"))
async def set_language(c: types.CallbackQuery):
    lang = c.data.split("_")[1]
    db["users"][c.from_user.id]["lang"] = lang
    await c.message.edit_text(STRINGS[lang]["menu"], reply_markup=get_main_kb(c.from_user.id))

@dp.callback_query(F.data.startswith("guide_"))
async def handle_guides(c: types.CallbackQuery):
    u_id = c.from_user.id
    g_type = c.data.split("_")[1]
    lang = db["users"][u_id]["lang"]
    await c.message.answer(GUIDES[lang][g_type], parse_mode="Markdown")
    await c.answer()

# --- GERİ BİLDİRİM ---
@dp.callback_query(F.data.startswith("fb_"))
async def handle_fb(c: types.CallbackQuery):
    u_id = c.from_user.id
    parts = c.data.split("_")
    status = "ÇALIŞIYOR ✅" if parts[1] == "ok" else "ÇALIŞMIYOR ❌"
    await bot.send_message(ADMIN_ID, f"📊 **Rapor:**\nKullanıcı: {c.from_user.full_name}\nTip: {parts[2]}\nDurum: {status}")
    await c.message.edit_text(STRINGS[db["users"][u_id]["lang"]]["thanks"])

# --- ADMIN PANELİ (Gelişmiş) ---
@dp.callback_query(F.data == "admin_home")
async def admin_home(c: types.CallbackQuery):
    if c.from_user.id != ADMIN_ID: return
    
    total = len(db["users"])
    pending = sum(1 for u in db["users"].values() if not u["approved"])
    active = sum(1 for u in db["users"].values() if u.get("active", True))
    
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="👤 Onay Bekleyenler", callback_data="admin_pending"))
    b.row(InlineKeyboardButton(text="📋 Kullanıcı Listesi", callback_data="admin_list"))
    b.row(InlineKeyboardButton(text="➕ VPN Ekle", callback_data="add_v"), InlineKeyboardButton(text="➕ Proxy Ekle", callback_data="add_p"))
    b.row(InlineKeyboardButton(text="🏠 Ana Menü", callback_data="back_main"))
    
    txt = f"🛡 **Admin Paneli**\n\n📊 Toplam: {total}\n⏳ Bekleyen: {pending}\n✅ Aktif: {active}\n\nVPN: {len(db['vpn_codes'])}\nProxy: {len(db['proxies'])}"
    await c.message.edit_text(txt, reply_markup=b.as_markup())

@dp.callback_query(F.data == "admin_list")
async def admin_list(c: types.CallbackQuery):
    txt = "📋 **Kullanıcılar:**\n"
    for uid, u in db["users"].items():
        txt += f"- {u['name']} (@{u['username']}) ID: {uid}\n"
    
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="⬅️ Geri", callback_data="admin_home"))
    await c.message.edit_text(txt[:4000], reply_markup=b.as_markup())

@dp.callback_query(F.data == "admin_pending")
async def admin_pending(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    count = 0
    for uid, u in db["users"].items():
        if not u["approved"]:
            b.row(InlineKeyboardButton(text=f"Onayla: {u['name']}", callback_data=f"approve_{uid}"))
            count += 1
    
    b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="admin_home"))
    await c.message.edit_text("Bekleyen kullanıcılar:" if count > 0 else "Bekleyen yok.", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("approve_"))
async def approve_user(c: types.CallbackQuery):
    uid = int(c.data.split("_")[1])
    db["users"][uid]["approved"] = True
    await bot.send_message(uid, "✅ Onaylandınız! /start yazarak başlayın.")
    await admin_pending(c)

@dp.callback_query(F.data == "back_main")
async def back_main(c: types.CallbackQuery):
    await c.message.edit_text(STRINGS[db["users"][c.from_user.id]["lang"]]["menu"], reply_markup=get_main_kb(c.from_user.id))

# --- MENÜ AYARLARI ---
async def startup_setup(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Başlat / Start"),
        BotCommand(command="/vpn", description="VPN Al"),
        BotCommand(command="/proxy", description="Proxy Al"),
        BotCommand(command="/help", description="Yardım / Kurulum")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def main():
    await startup_setup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
