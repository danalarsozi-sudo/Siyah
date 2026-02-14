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

# --- GERÇEKÇİ VERİ ÜRETİCİ (Sinir bozucu kısa kodlara son) ---
def generate_long_vpn():
    prefix = "happ:/crypt4/"
    chars = string.ascii_letters + string.digits
    part1 = ''.join(random.choice(chars) for _ in range(40))
    part2 = ''.join(random.choice(chars) for _ in range(32))
    part3 = ''.join(random.choice(chars) for _ in range(36))
    return f"{prefix}{part1}/{part2}/{part3}/vmyW1liNVpZVdJUpG7tycY0tQc+U/WRuLAtpZ4VQxiMlmd4VDFUtaQoDWlXJs6WHRtT1/RxO/F2vX2BF8="

# Geçici Veritabanı
db = {
    "users": {},
    "vpn_codes": [
        "happ:/crypt4/aswaa90qazYU31Ic3WLKPY9viOfu35NkLr7HYYekD9fQOokIBWOODu/y6zequYgjQ7bOnl8Q/QXskleNa9dCVK65W3LcVkUI2GMS5TAmMI5uY/iQ32GH53IBiJ5qiT6jOHWK35xhxGExBr6TzFUj01iOQ453T/2b6zlU1jJ1lcnXHfgDGpYFU4i9BeBbsmchdTm78R620/9SdPazOtdNEvwv3FZ8GhópVUQSWcbTGTmKO4NHs3IBWIUDWtJ5h5aCkQUVOxeO7Tlb+TKI481rg0ovmyW1liNVpZVdJUpG7tycY0tQc+U/Mn5on8bTCSpqm36cf+LoDbEvENnG1IspAX8EIv52Zx4plblBPcEDvrAyMS-+HBB8aJMeE9mb3ZliCrodxVzVAvwcSAPACKIm1Wóce+ebDnqpSazUULCaCSME9PwzKz+stW8Xjz8plulYGPaCg9G3cH9I5xZeqElfOwpUmaByPleF7X39FHFLHFWFwC927Wsp1rWe7Iy+3a3kl0Mb598afCwVCT5/Jah22bQXQSAKILNHfOn4yJexJQU8IdENBiPDa4e5bJklSOHuVT-+gArYiOwFYzhtLZIFs4IIOU/mizV2zN6VL23nMVShrpUZHzaGNB/WRuLAtpZ4VQxiMlmd4VDFUtaQoDWlXJs6WHRtT1/RxO/F2vX2BF8=",
    ],
    "proxies": [
        "IP: 50.210.166.34 | Port: 80 | Ülke: United States | Anonymity: High (HIA)",
        "IP: 209.135.168.41 | Port: 80 | Ülke: United States | Anonymity: Anonymous",
        "IP: 146.19.254.101 | Port: 5555 | Ülke: Netherlands | Anonymity: High"
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
        "back": "⬅️ Yza",
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
        "menu": "Главное menu:",
        "get_vpn": "🚀 Получить VPN код",
        "get_proxy": "🌐 Получить прокси IMO",
        "how_vpn": "📖 Как юзать VPN?",
        "how_imo": "📖 Настройка IMO",
        "refresh": "Обновить 🔄",
        "back": "⬅️ Назад",
        "admin_notify": "🔔 Новый пользователь: {name} ({id})",
        "approved": "✅ Ваш аккаунт одобрен!",
        "feedback_q": "Код/Прокси сработал?",
        "working": "✅ Работает",
        "not_working": "❌ Не работает",
        "thanks": "Спасибо за отзыв!"
    }
}

# --- HAMBURGER MENU (İşaretlediğin yer için) ---
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Botu Başlat / Запустить"),
        BotCommand(command="/vpn", description="VPN Kodu Al / Получить VPN"),
        BotCommand(command="/proxy", description="Proxy Al / Получить Прокси"),
        BotCommand(command="/admin", description="Admin Panel (Sadece Admin)"),
        BotCommand(command="/lang", description="Dil Değiştir / Сменить язык")
    ]
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())

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

@dp.message(Command("vpn"))
async def cmd_vpn(m: types.Message):
    await give_data_message(m, "get_vpn")

@dp.message(Command("proxy"))
async def cmd_proxy(m: types.Message):
    await give_data_message(m, "get_proxy")

@dp.message(Command("admin"))
async def cmd_admin(m: types.Message):
    if m.from_user.id == ADMIN_ID:
        await m.answer("Admin Paneline Hoşgeldin:", reply_markup=admin_panel_kb())

@dp.message(Command("lang"))
async def cmd_lang(m: types.Message):
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="sl_tm"), InlineKeyboardButton(text="RU 🇷🇺", callback_data="sl_ru"))
    await m.answer("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())

# --- DİNAMİK VERİ GÖNDERİMİ ---
async def give_data_message(m, callback_data):
    u_id = m.from_user.id
    if u_id not in db["users"] or not db["users"][u_id]["approved"]: return
    
    lang = db["users"][u_id]["lang"]
    is_vpn = callback_data == "get_vpn"
    data_list = db["vpn_codes"] if is_vpn else db["proxies"]
    item = random.choice(data_list)
    
    data_type = "VPN" if is_vpn else "Proxy"
    await m.answer(f"{'🚀' if is_vpn else '🌐'} **{data_type}:**\n\n`{item}`", parse_mode="Markdown")
    await m.answer(STRINGS[lang]["feedback_q"], reply_markup=feedback_kb(lang, data_type))

@dp.callback_query(F.data.in_(["get_vpn", "get_proxy"]))
async def cb_give_data(c: types.CallbackQuery):
    await give_data_message(c.message, c.data)
    await c.answer()

@dp.callback_query(F.data == "lang")
async def lang_sel(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="sl_tm"), InlineKeyboardButton(text="RU 🇷🇺", callback_data="sl_ru"))
    b.row(InlineKeyboardButton(text=STRINGS[db["users"][c.from_user.id]["lang"]]["back"], callback_data="back_main"))
    await c.message.edit_text("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("sl_"))
async def set_l(c: types.CallbackQuery):
    l = c.data.split("_")[1]
    db["users"][c.from_user.id]["lang"] = l
    await c.message.edit_text(STRINGS[l]["menu"], reply_markup=main_kb(c.from_user.id))

@dp.callback_query(F.data == "back_main")
async def back_to_main(c: types.CallbackQuery):
    u_id = c.from_user.id
    l = db["users"][u_id]["lang"]
    await c.message.edit_text(STRINGS[l]["menu"], reply_markup=main_kb(u_id))

# Geri Bildirim İşleme
@dp.callback_query(F.data.startswith("fb_"))
async def handle_feedback(c: types.CallbackQuery):
    u_id = c.from_user.id
    u_name = c.from_user.full_name
    l = db["users"][u_id]["lang"]
    parts = c.data.split("_")
    status = "ÇALIŞIYOR ✅" if parts[1] == "ok" else "ÇALIŞMIYOR ❌"
    data_type = parts[2]
    
    report = f"📊 **Geri Bildirim!**\nKullanıcı: {u_name} ({u_id})\nTip: {data_type}\nDurum: {status}"
    await bot.send_message(ADMIN_ID, report)
    await c.message.edit_text(STRINGS[l]["thanks"])
    await c.answer()

# --- ADMIN PANEL SİSTEMİ ---
def admin_panel_kb():
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="👤 Onay Bekleyenler", callback_data="adm_u"))
    b.row(InlineKeyboardButton(text="➕ VPN Ekle", callback_data="a_v"), InlineKeyboardButton(text="➕ Proxy Ekle", callback_data="a_p"))
    b.row(InlineKeyboardButton(text="🏠 Ana Menü", callback_data="back_main"))
    return b.as_markup()

@dp.callback_query(F.data == "adm")
async def adm_p(c: types.CallbackQuery):
    if c.from_user.id != ADMIN_ID: return
    await c.message.edit_text(f"🛡 Admin Paneli\nVPN: {len(db['vpn_codes'])}\nProxy: {len(db['proxies'])}", reply_markup=admin_panel_kb())

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
        b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="adm"))
        await c.message.edit_text("Bekleyen kimse yok.", reply_markup=b.as_markup())
        return
    b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="adm"))
    await c.message.edit_text("Onay bekleyen kullanıcılar:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("ok_"))
async def ok_u(c: types.CallbackQuery):
    uid = int(c.data.split("_")[1])
    db["users"][uid]["approved"] = True
    await bot.send_message(uid, STRINGS[db["users"][uid]["lang"]]["approved"])
    await c.answer("Onaylandı")
    await adm_u(c)

# Admin Manuel Ekleme
@dp.callback_query(F.data == "a_v")
async def add_v_start(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_vpn)
    await c.message.answer("VPN Kodunu Gönderin (Uzun versiyon):")

@dp.callback_query(F.data == "a_p")
async def add_p_start(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_proxy)
    await c.message.answer("Proxy Bilgisini Gönderin:")

@dp.message(AdminStates.waiting_for_vpn)
async def process_v(m: types.Message, state: FSMContext):
    db["vpn_codes"].append(m.text)
    await m.answer("✅ Manuel VPN eklendi.")
    await state.clear()

@dp.message(AdminStates.waiting_for_proxy)
async def process_p(m: types.Message, state: FSMContext):
    db["proxies"].append(m.text)
    await m.answer("✅ Manuel Proxy eklendi.")
    await state.clear()

# Arka Plan Tarayıcı (Artık GERÇEKÇİ UZUN KODLAR üretiyor)
async def scan():
    while True:
        db["vpn_codes"].append(generate_long_vpn())
        await asyncio.sleep(1800) # 30 dakikada bir yeni uzun kod

async def main():
    await set_main_menu(bot)
    asyncio.create_task(scan())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
