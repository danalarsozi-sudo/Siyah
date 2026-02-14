import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
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

# Geçici Veritabanı
db = {
    "users": {},
    "vpn_codes": [
        "happ:/crypt4/aswaa90qazYU31Ic3WLKPY9viOfu35NkLr7HYYekD9fQOokIBWOODu/y6zequYgjQ7bOnl8Q/...",
    ],
    "proxies": [
        "IP: 50.210.166.34 | Port: 80 | USA",
        "IP: 146.19.254.101 | Port: 5555 | Netherlands"
    ]
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- DİL SÖZLÜĞÜ ---
STRINGS = {
    "tm": {
        "welcome": "Salam! Bu bot size mugt Happ VPN kodlaryny we IMO proksilerini berýär.",
        "need_auth": f"Siz entek tassyklanmadyňyz. Admin bilen habarlaşyň: {ADMIN_USERNAME}",
        "menu": "Esasy Menýu:",
        "get_vpn": "🚀 VPN Kodyny al",
        "get_proxy": "🌐 IMO Proksisini al",
        "how_vpn": "📖 VPN ulanmak",
        "how_imo": "📖 IMO Proksi sazlamak",
        "refresh": "Tazelemek 🔄",
        "admin_notify": "🔔 Täze ulanyjy: {name} ({id})",
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
        "how_vpn": "📖 Как юзать VPN?",
        "how_imo": "📖 Настройка IMO",
        "refresh": "Обновить 🔄",
        "admin_notify": "🔔 Новый пользователь: {name} ({id})",
        "approved": "✅ Ваш аккаунт одобрен!",
        "feedback_q": "Код/Прокси сработал?",
        "working": "✅ Работает",
        "not_working": "❌ Не работает",
        "thanks": "Спасибо за отзыв!"
    }
}

# --- KLAVYELER ---
def main_kb(u_id):
    lang = db["users"].get(u_id, {}).get("lang", "tm")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=STRINGS[lang]["get_vpn"], callback_data="get_vpn"))
    builder.row(InlineKeyboardButton(text=STRINGS[lang]["get_proxy"], callback_data="get_proxy"))
    builder.row(InlineKeyboardButton(text=STRINGS[lang]["how_vpn"], callback_data="h_v"),
                InlineKeyboardButton(text=STRINGS[lang]["how_imo"], callback_data="h_i"))
    builder.row(InlineKeyboardButton(text="🌍 Dil / Язык", callback_data="lang"))
    if u_id == ADMIN_ID:
        builder.row(InlineKeyboardButton(text="🛡 Admin Panel", callback_data="adm"))
    return builder.as_markup()

def feedback_kb(lang, data_type):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=STRINGS[lang]["working"], callback_data=f"fb_ok_{data_type}"))
    builder.add(InlineKeyboardButton(text=STRINGS[lang]["not_working"], callback_data=f"fb_no_{data_type}"))
    return builder.as_markup()

# --- HANDLERS ---
@dp.message(Command("start"))
async def start(m: types.Message):
    u_id = m.from_user.id
    if u_id not in db["users"]:
        db["users"][u_id] = {"approved": (u_id == ADMIN_ID), "lang": "tm", "name": m.from_user.full_name}
        await bot.send_message(ADMIN_ID, STRINGS["tm"]["admin_notify"].format(name=m.from_user.full_name, id=u_id))

    user = db["users"][u_id]
    if not user["approved"]:
        await m.answer(STRINGS["tm"]["need_auth"])
        return
    await m.answer(STRINGS[user["lang"]]["welcome"], reply_markup=main_kb(u_id))

@dp.callback_query(F.data == "lang")
async def lang_sel(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="sl_tm"), InlineKeyboardButton(text="RU 🇷🇺", callback_data="sl_ru"))
    await c.message.edit_text("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("sl_"))
async def set_l(c: types.CallbackQuery):
    l = c.data.split("_")[1]
    db["users"][c.from_user.id]["lang"] = l
    await c.message.edit_text(STRINGS[l]["menu"], reply_markup=main_kb(c.from_user.id))

# VPN/Proxy Gönderimi
@dp.callback_query(F.data.in_(["get_vpn", "get_proxy"]))
async def give_data(c: types.CallbackQuery):
    u_id = c.from_user.id
    l = db["users"][u_id]["lang"]
    is_vpn = c.data == "get_vpn"
    data_list = db["vpn_codes"] if is_vpn else db["proxies"]
    item = random.choice(data_list)
    
    # Bilgi mesajı
    data_type = "VPN" if is_vpn else "Proxy"
    await c.message.answer(f"{'🚀' if is_vpn else '🌐'} **{data_type}:**\n\n`{item}`", parse_mode="Markdown")
    
    # Geri bildirim butonları
    await c.message.answer(STRINGS[l]["feedback_q"], reply_markup=feedback_kb(l, data_type))
    await c.answer()

# Geri Bildirim İşleme
@dp.callback_query(F.data.startswith("fb_"))
async def handle_feedback(c: types.CallbackQuery):
    u_id = c.from_user.id
    u_name = c.from_user.full_name
    l = db["users"][u_id]["lang"]
    parts = c.data.split("_")
    status = "ÇALIŞIYOR ✅" if parts[1] == "ok" else "ÇALIŞMIYOR ❌"
    data_type = parts[2]
    
    # Admine raporla
    report = f"📊 **Geri Bildirim!**\nKullanıcı: {u_name} ({u_id})\nTip: {data_type}\nDurum: {status}"
    await bot.send_message(ADMIN_ID, report)
    
    # Kullanıcıya teşekkür et ve butonları kaldır
    await c.message.edit_text(STRINGS[l]["thanks"])
    await c.answer()

# --- ADMIN PANEL ---
@dp.callback_query(F.data == "adm")
async def adm_p(c: types.CallbackQuery):
    if c.from_user.id != ADMIN_ID: return
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="Onay Bekleyenler", callback_data="adm_u"))
    b.row(InlineKeyboardButton(text="➕ VPN Ekle", callback_data="a_v"), InlineKeyboardButton(text="➕ Proxy Ekle", callback_data="a_p"))
    await c.message.edit_text(f"🛡 Admin Paneli\nVPN Sayısı: {len(db['vpn_codes'])}\nProxy Sayısı: {len(db['proxies'])}", reply_markup=b.as_markup())

@dp.callback_query(F.data == "adm_u")
async def adm_u(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    count = 0
    for uid, u in db["users"].items():
        if not u["approved"]:
            b.row(InlineKeyboardButton(text=f"Onayla: {u['name']}", callback_data=f"ok_{uid}"))
            count += 1
    if count == 0:
        await c.answer("Bekleyen kullanıcı yok.")
        return
    b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="adm"))
    await c.message.edit_text("Onay bekleyen kullanıcılar:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("ok_"))
async def ok_u(c: types.CallbackQuery):
    uid = int(c.data.split("_")[1])
    db["users"][uid]["approved"] = True
    await bot.send_message(uid, STRINGS[db["users"][uid]["lang"]]["approved"])
    await c.answer("Kullanıcı onaylandı")
    await adm_u(c)

# Admin Manuel Ekleme
@dp.callback_query(F.data == "a_v")
async def add_v_start(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_vpn)
    await c.message.answer("Lütfen yeni VPN kodunu gönderin:")

@dp.callback_query(F.data == "a_p")
async def add_p_start(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_proxy)
    await c.message.answer("Lütfen yeni Proxy bilgisini gönderin:")

@dp.message(AdminStates.waiting_for_vpn)
async def process_v(m: types.Message, state: FSMContext):
    db["vpn_codes"].append(m.text)
    await m.answer("✅ VPN kodu eklendi.")
    await state.clear()

@dp.message(AdminStates.waiting_for_proxy)
async def process_p(m: types.Message, state: FSMContext):
    db["proxies"].append(m.text)
    await m.answer("✅ Proxy eklendi.")
    await state.clear()

# Arka Plan Tarayıcı (Simüle)
async def scan():
    while True:
        db["vpn_codes"].append(f"happ:/auto-scan-{random.randint(100,999)}")
        await asyncio.sleep(3600)

async def main():
    asyncio.create_task(scan())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
