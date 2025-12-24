from telethon import events, Button
from enums import UserState
from database.user_repo import set_state
from database.settings_repo import get_products
from config import ADMIN_ID

def register(bot):
    # دقت کنید که فقط همین یک تابع برای /start در کل پروژه باشد
    @bot.on(events.NewMessage(pattern=r"(?i)^/start$"))
    async def start_handler(event):
        # 1. تنظیم وضعیت کاربر در دیتابیس
        await set_state(event.sender_id, UserState.START)
        
        # 2. دریافت پکیج‌های تعریف شده توسط ادمین از دیتابیس
        products = await get_products()
        
        # 3. ساخت دکمه‌ها بر اساس دیتای دیتابیس
        buttons = []
        for p_id, p_info in products.items():
            # نام دکمه از دیتابیس می‌آید (تغییراتی که در پنل دادی اینجا اعمال می‌شود)
            buttons.append([Button.inline(f"📦 {p_info['name']}", p_id.encode())])
        
        # 4. دکمه پنل مدیریت فقط برای ادمین
        if event.sender_id == ADMIN_ID:
            buttons.append([Button.inline("🛡 ورود به پنل مدیریت", b"admin_menu")])

        # 5. ارسال پیام خوش‌آمدگویی
        await event.respond(
            "سلام 👋 خوش آمدید.\nلطفاً پک مورد نظر خود را انتخاب کنید:", 
            buttons=buttons
        )

    # پاسخ به دکمه پنل مدیریت
    @bot.on(events.CallbackQuery(data=b"admin_menu"))
    async def fast_admin(event):
        await event.respond("🛡 برای مدیریت ربات دستور /admin را ارسال کنید.")