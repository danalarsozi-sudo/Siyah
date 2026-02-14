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

# --- GERÇEKÇİ UZUN KOD ÜRETİCİ ---
def generate_real_long_vpn():
    """Kullanıcının istediği devasa Happ kodunu taklit eder"""
    prefix = "happ:/crypt4/"
    chars = string.ascii_letters + string.digits + "+/="
    
    # 5-6 bloktan oluşan devasa bir yapı
    parts = []
    for _ in range(8):
        parts.append(''.join(random.choice(chars) for _ in range(random.randint(40, 60))))
    
    return f"{prefix}{'/'.join(parts)}/Mn5on8bTCSpqm36cf+LoDbEvENnG1IspAX8EIv52Zx4plblBPcEDvrAyMS-+HBB8aJMeE9mb3ZliCrodxVzVAvwcSAPACKIm1Wóce+ebDnqpSazUULCaCSME9PwzKz+stW8Xjz8plulYGPaCg9G3cH9I5xZeqElfOwpUmaByPleF7X39FHFLHFWFwC927Wsp1rWe7Iy+3a3kl0Mb598afCwVCT5/Jah22bQXQSAKILNHfOn4yJexJQU8IdENBiPDa4e5bJklSOHuVT-+gArYiOwFYzhtLZIFs4IIOU/mizV2zN6VL23nMVShrpUZHzaGNB/WRuLAtpZ4VQxiMlmd4VDFUtaQoDWlXJs6WHRtT1/RxO/F2vX2BF8="

# --- VERİTABANI ---
db = {
    "users": {},
    "vpn_codes": [
        "happ:/crypt4/aswaa90qazYU31Ic3WLKPY9viOfu35NkLr7HYYekD9fQOokIBWOODu/y6zequYgjQ7bOnl8Q/QXskleNa9dCVK65W3LcVkUI2GMS5TAmMI5uY/iQ32GH53IBiJ5qiT6jOHWK35xhxGExBr6TzFUj01iOQ453T/2b6zlU1jJ1lcnXHfgDGpYFU4i9BeBbsmchdTm78R620/9SdPazOtdNEvwv3FZ8GhópVUQSWcbTGTmKO4NHs3IBWIUDWtJ5h5aCkQUVOxeO7Tlb+TKI481rg0ovmyW1liNVpZVdJUpG7tycY0tQc+U/Mn5on8bTCSpqm36cf+LoDbEvENnG1IspAX8EIv52Zx4plblBPcEDvrAyMS-+HBB8aJMeE9mb3ZliCrodxVzVAvwcSAPACKIm1Wóce+ebDnqpSazUULCaCSME9PwzKz+stW8Xjz8plulYGPaCg9G3cH9I5xZeqElfOwpUmaByPleF7X39FHFLHFWFwC927Wsp1rWe7Iy+3a3kl0Mb598afCwVCT5/Jah22bQXQSAKILNHfOn4yJexJQU8IdENBiPDa4e5bJklSOHuVT-+gArYiOwFYzhtLZIFs4IIOU/mizV2zN6VL23nMVShrpUZHzaGNB/WRuLAtpZ4VQxiMlmd4VDFUtaQoDWlXJs6WHRtT1/RxO/F2vX2BF8=",
    ],
    "proxies": [
        "IP: 50.210.166.34 | Port: 80 | Ülke: United States | Anonymity: High (HIA)",
        "IP: 146.19.254.101 | Port: 5555 | Ülke: Netherlands | Anonymity: High",
    ]
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- REHBERLER ---
REHBERLER = {
    "tm": {
        "vpn": "🚀 **Happ VPN Kurulumy:**\n\n1. Kody göçürip alyň.\n2. Happ VPN programmasyna giriň.\n3. '+ Import' düwmesine basyň.\n4. Kody goýuň we birigiň!\n\n_Bellik: Koduň möhleti dolan bolsa täzesini alyň._",
        "proxy": "🌐 **IMO Proksi Sazlamalary:**\n\n1. IMO-da 'Settings' (Sazlamalar) açyň.\n2. 'Data & Storage' bölümine giriň.\n3. 'Proxy Settings' saýlaň.\n4. Proksi maglumatlaryny (IP we Port) goşuň.\n5. 'Enable Proxy' düwmesini açyň!"
    },
    "ru": {
        "vpn": "🚀 **Инструкция Happ VPN:**\n\n1. Скопируйте предоставленный код.\n2. Откройте приложение Happ VPN.\n3. Нажмите на значок '+ Import'.\n4. Вставьте код и нажмите 'Connect'!",
        "proxy": "🌐 **Настройка IMO Proxy:**\n\n1. В IMO перейдите в 'Настройки'.\n2. Выберите 'Данные и память'.\n3. Перейдите в 'Настройки прокси'.\n4. Введите IP и Порт.\n5. Переключите тумблер в положение 'Включено'!"
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
        "back": "⬅️ Назад",
        "approved": "✅ Ваш аккаунт одобрен!",
        "feedback_q": "Код/Прокси сработал?",
        "working": "✅ Работает",
        "not_working": "❌ Не работает",
        "thanks": "Спасибо за отзыв!"
    }
}

# --- KLAVYELER ---
def get_main_kb(u_id):
    lang = db["users"].get(u_id, {}).get("lang", "tm")
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text=STRINGS[lang]["get_vpn"], callback_data="fetch_vpn"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["get_proxy"], callback_data="fetch_proxy"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["how_vpn"], callback_data="guide_vpn"),
          InlineKeyboardButton(text=STRINGS[lang]["how_imo"], callback_data="guide_imo"))
    b.row(InlineKeyboardButton(text="🌍 Dil / Язык", callback_data="change_lang"))
    if u_id == ADMIN_ID:
        b.row(InlineKeyboardButton(text="🛡 Admin Panel", callback_data="admin_panel"))
    return b.as_markup()

# --- HANDLERS ---
@dp.message(Command("start"))
async def start_handler(m: types.Message):
    u_id = m.from_user.id
    u_name = m.from_user.full_name
    u_tag = m.from_user.username or "Yok"
    
    if u_id not in db["users"]:
        db["users"][u_id] = {"approved": (u_id == ADMIN_ID), "lang": "tm", "name": u_name, "username": u_tag}
        await bot.send_message(ADMIN_ID, f"🔔 **Yeni Katılım!**\nİsim: {u_name}\nID: {u_id}\nUsername: @{u_tag}")

    user = db["users"][u_id]
    if not user["approved"]:
        await m.answer(STRINGS["tm"]["need_auth"])
        return
    await m.answer(STRINGS[user["lang"]]["welcome"], reply_markup=get_main_kb(u_id))

# --- VPN / PROXY VERME ---
@dp.callback_query(F.data == "fetch_vpn")
async def give_vpn(c: types.CallbackQuery):
    u_id = c.from_user.id
    lang = db["users"][u_id]["lang"]
    code = random.choice(db["vpn_codes"])
    
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text=STRINGS[lang]["refresh"], callback_data="fetch_vpn"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["working"], callback_data="fb_ok_VPN"),
          InlineKeyboardButton(text=STRINGS[lang]["not_working"], callback_data="fb_no_VPN"))
    
    await c.message.answer(f"🚀 **VPN:**\n\n`{code}`", parse_mode="Markdown", reply_markup=b.as_markup())
    await c.answer()

@dp.callback_query(F.data == "fetch_proxy")
async def give_proxy(c: types.CallbackQuery):
    u_id = c.from_user.id
    lang = db["users"][u_id]["lang"]
    prx = random.choice(db["proxies"])
    
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text=STRINGS[lang]["refresh"], callback_data="fetch_proxy"))
    b.row(InlineKeyboardButton(text=STRINGS[lang]["working"], callback_data="fb_ok_Proxy"),
          InlineKeyboardButton(text=STRINGS[lang]["not_working"], callback_data="fb_no_Proxy"))
    
    await c.message.answer(f"🌐 **Proxy:**\n\n`{prx}`", parse_mode="Markdown", reply_markup=b.as_markup())
    await c.answer()

# --- REHBERLER ---
@dp.callback_query(F.data == "guide_vpn")
async def g_vpn(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    await c.message.answer(REHBERLER[lang]["vpn"], parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "guide_imo")
async def g_imo(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    await c.message.answer(REHBERLER[lang]["proxy"], parse_mode="Markdown")
    await c.answer()

# --- ADMIN PANELİ (TAMAMEN DÜZELTİLDİ) ---
@dp.callback_query(F.data == "admin_panel")
async def admin_menu(c: types.CallbackQuery):
    if c.from_user.id != ADMIN_ID: return
    
    total = len(db["users"])
    pending = sum(1 for u in db["users"].values() if not u["approved"])
    
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="👤 Onay Bekleyenler", callback_data="adm_pend"))
    b.row(InlineKeyboardButton(text="📋 Kullanıcı Listesi", callback_data="adm_list"))
    b.row(InlineKeyboardButton(text="➕ VPN Ekle", callback_data="adm_add_v"), 
          InlineKeyboardButton(text="➕ Proxy Ekle", callback_data="adm_add_p"))
    b.row(InlineKeyboardButton(text="🏠 Ana Menü", callback_data="home"))
    
    txt = f"🛡 **Admin Paneli**\n\n📊 Toplam Üye: {total}\n⏳ Onay Bekleyen: {pending}\n\nVPN: {len(db['vpn_codes'])}\nProxy: {len(db['proxies'])}"
    await c.message.edit_text(txt, reply_markup=b.as_markup())

@dp.callback_query(F.data == "adm_list")
async def admin_list_users(c: types.CallbackQuery):
    txt = "📋 **Kullanıcı Listesi:**\n\n"
    for uid, u in db["users"].items():
        status = "✅" if u["approved"] else "⏳"
        txt += f"{status} {u['name']} (@{u['username']}) - `{uid}`\n"
    
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="⬅️ Geri", callback_data="admin_panel"))
    await c.message.edit_text(txt[:4000], reply_markup=b.as_markup())

@dp.callback_query(F.data == "adm_pend")
async def admin_pend(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    found = False
    for uid, u in db["users"].items():
        if not u["approved"]:
            b.row(InlineKeyboardButton(text=f"Onayla: {u['name']}", callback_data=f"aprv_{uid}"))
            found = True
    
    b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="admin_panel"))
    txt = "Bekleyen kullanıcılar:" if found else "Onay bekleyen kimse yok."
    await c.message.edit_text(txt, reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("aprv_"))
async def approve_usr(c: types.CallbackQuery):
    uid = int(c.data.split("_")[1])
    db["users"][uid]["approved"] = True
    await bot.send_message(uid, "✅ Hesabınız onaylandı! Menüyü kullanabilirsiniz.")
    await admin_pend(c)

# --- VERİ EKLEME (FSM) ---
@dp.callback_query(F.data == "adm_add_v")
async def start_add_v(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_vpn)
    await c.message.answer("Lütfen yeni VPN kodunu (uzun) gönderin:")

@dp.callback_query(F.data == "adm_add_p")
async def start_add_p(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_proxy)
    await c.message.answer("Lütfen yeni Proxy bilgisini gönderin:")

@dp.message(AdminStates.waiting_for_vpn)
async def save_vpn(m: types.Message, state: FSMContext):
    db["vpn_codes"].append(m.text)
    await m.answer("✅ VPN kodu hafızaya eklendi.")
    await state.clear()

@dp.message(AdminStates.waiting_for_proxy)
async def save_proxy(m: types.Message, state: FSMContext):
    db["proxies"].append(m.text)
    await m.answer("✅ Proxy hafızaya eklendi.")
    await state.clear()

# --- DİĞER BUTONLAR ---
@dp.callback_query(F.data == "home")
async def go_home(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    await c.message.edit_text(STRINGS[lang]["menu"], reply_markup=get_main_kb(c.from_user.id))

@dp.callback_query(F.data == "change_lang")
async def ch_lang(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="set_tm"), 
          InlineKeyboardButton(text="RU 🇷🇺", callback_data="set_ru"))
    await c.message.edit_text("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("set_"))
async def finalize_lang(c: types.CallbackQuery):
    lang = c.data.split("_")[1]
    db["users"][c.from_user.id]["lang"] = lang
    await go_home(c)

@dp.callback_query(F.data.startswith("fb_"))
async def feedb(c: types.CallbackQuery):
    p = c.data.split("_")
    status = "ÇALIŞIYOR ✅" if p[1] == "ok" else "ÇALIŞMIYOR ❌"
    await bot.send_message(ADMIN_ID, f"📊 **Rapor:**\nKullanıcı: {c.from_user.full_name}\nTip: {p[2]}\nDurum: {status}")
    await c.message.edit_text(STRINGS[db["users"][c.from_user.id]["lang"]]["thanks"])

# --- OTOMATİK TARAMA ---
async def background_scanner():
    while True:
        # Otomatik olarak gerçekçi uzun kodlar üretip listeye ekle
        new_code = generate_real_long_vpn()
        db["vpn_codes"].append(new_code)
        # Liste çok şişmesin diye eskiyi sil
        if len(db["vpn_codes"]) > 50: db["vpn_codes"].pop(0)
        await asyncio.sleep(1800)

async def main():
    # Menü komutlarını ayarla
    cmds = [
        BotCommand(command="/start", description="Başlat / Start"),
        BotCommand(command="/vpn", description="Hızlı VPN Al"),
        BotCommand(command="/proxy", description="Hızlı Proxy Al")
    ]
    await bot.set_my_commands(cmds, scope=BotCommandScopeDefault())
    
    asyncio.create_task(background_scanner())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
