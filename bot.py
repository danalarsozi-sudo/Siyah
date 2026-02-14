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
from aiogram.exceptions import TelegramForbiddenError

# --- KONFİGÜRASYON ---
API_TOKEN = '8131658723:AAGgWDY75CuZvk88EHDemJzEBKhIW77m3ZY'
ADMIN_ID = 1748533804
ADMIN_USERNAME = "@Eminvb"

logging.basicConfig(level=logging.INFO)

class AdminStates(StatesGroup):
    waiting_for_vpn = State()
    waiting_for_proxy = State()

# --- VERİTABANI ---
db = {
    "users": {},
    "vpn_codes": [
        "happ:/crypt4/aswaa90qazYU31Ic3WLKPY9viOfu35NkLr7HYYekD9fQOokIBWOODu/y6zequYgjQ7bOnl8Q/QXskleNa9dCVK65W3LcVkUI2GMS5TAmMI5uY/iQ32GH53IBiJ5qiT6jOHWK35xhxGExBr6TzFUj01iOQ453T/2b6zlU1jJ1lcnXHfgDGpYFU4i9BeBbsmchdTm78R620/9SdPazOtdNEvwv3FZ8GhópVUQSWcbTGTmKO4NHs3IBWIUDWtJ5h5aCkQUVOxeO7Tlb+TKI481rg0ovmyW1liNVpZVdJUpG7tycY0tQc+U/Mn5on8bTCSpqm36cf+LoDbEvENnG1IspAX8EIv52Zx4plblBPcEDvrAyMS-+HBB8aJMeE9mb3ZliCrodxVzVAvwcSAPACKIm1Wóce+ebDnqpSazUULCaCSME9PwzKz+stW8Xjz8plulYGPaCg9G3cH9I5xZeqElfOwpUmaByPleF7X39FHFLHFWFwC927Wsp1rWe7Iy+3a3kl0Mb598afCwVCT5/Jah22bQXQSAKILNHfOn4yJexJQU8IdENBiPDa4e5bJklSOHuVT-+gArYiOwFYzhtLZIFs4IIOU/mizV2zN6VL23nMVShrpUZHzaGNB/WRuLAtpZ4VQxiMlmd4VDFUtaQoDWlXJs6WHRtT1/RxO/F2vX2BF8=",
    ],
    "proxies": [
        "IP: 50.210.166.34 | Port: 80 | Ülke: USA | Anonymity: High",
        "IP: 146.19.254.101 | Port: 5555 | Ülke: Netherlands",
    ],
    "deleted_count": 0
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- REHBERLER ---
GUIDES = {
    "tm": {
        "vpn": "🚀 **Happ VPN Kurulumy:**\n1. Kody göçürip alyň.\n2. Happ VPN programmasyna giriň.\n3. '+ Import' düwmesine basyň.\n4. Kody goýuň we birigiň!",
        "proxy": "🌐 **IMO Proksi Kurulumy:**\n1. Sazlamalara giriň.\n2. 'Data & Storage' saýlaň.\n3. 'Proxy Settings' basyň.\n4. Proksini goşuň!"
    },
    "ru": {
        "vpn": "🚀 **Установка Happ VPN:**\n1. Скопируйте код.\n2. Откройте Happ VPN.\n3. Нажмите '+ Import'.\n4. Вставьте и подключайтесь!",
        "proxy": "🌐 **Настройка IMO Proxy:**\n1. В IMO зайдите в Настройки.\n2. 'Данные и память' -> 'Настройки прокси'.\n3. Введите данные!"
    }
}

# --- YARDIMCI FONKSİYONLAR ---
def get_main_kb(u_id):
    lang = db["users"].get(u_id, {}).get("lang", "tm")
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🚀 VPN Kodyny al / Получить VPN", callback_data="get_vpn_data"))
    b.row(InlineKeyboardButton(text="🌐 IMO Proksisini al / Получить Proxy", callback_data="get_proxy_data"))
    b.row(InlineKeyboardButton(text="📖 VPN Guide", callback_data="guide_v"), InlineKeyboardButton(text="📖 IMO Guide", callback_data="guide_p"))
    b.row(InlineKeyboardButton(text="🌍 Dil / Язык", callback_data="change_language"))
    if u_id == ADMIN_ID:
        b.row(InlineKeyboardButton(text="🛡 Admin Panel", callback_data="open_admin"))
    return b.as_markup()

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    u_id = m.from_user.id
    if u_id not in db["users"]:
        db["users"][u_id] = {"approved": (u_id == ADMIN_ID), "lang": "tm", "name": m.from_user.full_name, "username": m.from_user.username}
        await bot.send_message(ADMIN_ID, f"🔔 **Täze ulanyjy:** {m.from_user.full_name} (@{m.from_user.username})")
    
    user = db["users"][u_id]
    if not user["approved"]:
        await m.answer(f"Siz entek tassyklanmadyňyz. Admin: {ADMIN_USERNAME}")
        return
    await m.answer("Esasy Menýu / Главное меню:", reply_markup=get_main_kb(u_id))

# --- VERI VERME BUTONLARI (KESİN ÇÖZÜM) ---
@dp.callback_query(F.data == "get_vpn_data")
async def send_vpn(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    code = random.choice(db["vpn_codes"])
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🔄 Tazelemek / Обновить", callback_data="get_vpn_data"))
    b.row(InlineKeyboardButton(text="✅ Işledi / Работает", callback_data="fb_ok_VPN"), 
          InlineKeyboardButton(text="❌ İşlemedi / Не работает", callback_data="fb_no_VPN"))
    await c.message.answer(f"🚀 **VPN:**\n\n`{code}`", parse_mode="Markdown", reply_markup=b.as_markup())
    await c.answer()

@dp.callback_query(F.data == "get_proxy_data")
async def send_proxy(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    item = random.choice(db["proxies"])
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🔄 Tazelemek / Обновить", callback_data="get_proxy_data"))
    b.row(InlineKeyboardButton(text="✅ Işledi / Работает", callback_data="fb_ok_Proxy"), 
          InlineKeyboardButton(text="❌ İşlemedi / Не работает", callback_data="fb_no_Proxy"))
    await c.message.answer(f"🌐 **Proxy:**\n\n`{item}`", parse_mode="Markdown", reply_markup=b.as_markup())
    await c.answer()

# --- REHBER BUTONLARI ---
@dp.callback_query(F.data == "guide_v")
async def g_v(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    await c.message.answer(GUIDES[lang]["vpn"], parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "guide_p")
async def g_p(c: types.CallbackQuery):
    lang = db["users"][c.from_user.id]["lang"]
    await c.message.answer(GUIDES[lang]["proxy"], parse_mode="Markdown")
    await c.answer()

# --- ADMIN HOME ---
@dp.callback_query(F.data == "open_admin")
async def admin_home(c: types.CallbackQuery):
    if c.from_user.id != ADMIN_ID: return
    total = len(db["users"])
    pending = sum(1 for u in db["users"].values() if not u["approved"])
    
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="⏳ Bekleyenler", callback_data="adm_pend"), InlineKeyboardButton(text="📋 Liste", callback_data="adm_list"))
    b.row(InlineKeyboardButton(text="➕ VPN Ekle", callback_data="adm_add_v"), InlineKeyboardButton(text="➕ Proxy Ekle", callback_data="adm_add_p"))
    b.row(InlineKeyboardButton(text="🏠 Başlangıç", callback_data="back_home"))
    
    await c.message.edit_text(f"🛡 **Admin**\nTop: {total} | Bekleyen: {pending}\nSilen/Engellenen: {db['deleted_count']}", reply_markup=b.as_markup())

@dp.callback_query(F.data == "adm_list")
async def adm_list(c: types.CallbackQuery):
    txt = "📋 **Kullanıcılar:**\n"
    for uid, u in db["users"].items():
        txt += f"- {u['name']} (@{u['username']}) ID: `{uid}`\n"
    b = InlineKeyboardBuilder().add(InlineKeyboardButton(text="⬅️ Geri", callback_data="open_admin"))
    await c.message.edit_text(txt[:4000], reply_markup=b.as_markup())

@dp.callback_query(F.data == "adm_pend")
async def adm_pend(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    for uid, u in db["users"].items():
        if not u["approved"]: b.row(InlineKeyboardButton(text=f"Onayla: {u['name']}", callback_data=f"aprv_{uid}"))
    b.row(InlineKeyboardButton(text="⬅️ Geri", callback_data="open_admin"))
    await c.message.edit_text("Onay bekleyenler:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("aprv_"))
async def aprv(c: types.CallbackQuery):
    uid = int(c.data.split("_")[1])
    db["users"][uid]["approved"] = True
    try: await bot.send_message(uid, "✅ Hesabınız onaylandı!")
    except TelegramForbiddenError: db["deleted_count"] += 1
    await adm_pend(c)

# --- VERİ EKLEME VE SİLME ---
@dp.callback_query(F.data == "adm_add_v")
async def add_v_st(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_vpn)
    await c.message.answer("Yeni VPN kodunu gönderin:")

@dp.callback_query(F.data == "adm_add_p")
async def add_p_st(c: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_proxy)
    await c.message.answer("Yeni Proxy bilgisini gönderin:")

@dp.message(AdminStates.waiting_for_vpn)
async def save_v(m: types.Message, state: FSMContext):
    db["vpn_codes"].append(m.text)
    b = InlineKeyboardBuilder().add(InlineKeyboardButton(text="🗑 Bu Kaydı Sil", callback_data="del_last_vpn"))
    await m.answer("✅ VPN eklendi!", reply_markup=b.as_markup())
    await state.clear()

@dp.message(AdminStates.waiting_for_proxy)
async def save_p(m: types.Message, state: FSMContext):
    db["proxies"].append(m.text)
    b = InlineKeyboardBuilder().add(InlineKeyboardButton(text="🗑 Bu Kaydı Sil", callback_data="del_last_proxy"))
    await m.answer("✅ Proxy eklendi!", reply_markup=b.as_markup())
    await state.clear()

@dp.callback_query(F.data.startswith("del_last_"))
async def del_last(c: types.CallbackQuery):
    target = c.data.split("_")[2]
    if target == "vpn": db["vpn_codes"].pop()
    else: db["proxies"].pop()
    await c.message.edit_text("❌ Kayıt başarıyla silindi.")

# --- DİĞER ---
@dp.callback_query(F.data == "back_home")
async def b_h(c: types.CallbackQuery):
    await c.message.edit_text("Esasy Menýu:", reply_markup=get_main_kb(c.from_user.id))

@dp.callback_query(F.data == "change_language")
async def ch_l(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.add(InlineKeyboardButton(text="TM 🇹🇲", callback_data="sl_tm"), InlineKeyboardButton(text="RU 🇷🇺", callback_data="sl_ru"))
    await c.message.edit_text("Dil saýlaň / Выберите язык:", reply_markup=b.as_markup())

@dp.callback_query(F.data.startswith("sl_"))
async def finalize_l(c: types.CallbackQuery):
    db["users"][c.from_user.id]["lang"] = c.data.split("_")[1]
    await b_h(c)

@dp.callback_query(F.data.startswith("fb_"))
async def fb_h(c: types.CallbackQuery):
    p = c.data.split("_")
    status = "✅" if p[1] == "ok" else "❌"
    await bot.send_message(ADMIN_ID, f"📊 **Rapor:** {c.from_user.full_name} | {p[2]} | {status}")
    await c.message.edit_text("Sag boluň! / Спасибо!")

async def main():
    await bot.set_my_commands([BotCommand(command="/start", description="Başlat")], scope=BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
