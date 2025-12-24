from telethon import events, Button
from enums import UserState
from database.user_repo import get_state, set_state
from database.order_repo import update_order
from config import ADMIN_ID

def register(bot):
    # این هندلر فقط زمانی کار می‌کند که کاربر عکسی بفرستد
    @bot.on(events.NewMessage)
    async def receipt_handler(event):
        # 1. بررسی وضعیت کاربر (فقط اگر منتظر فیش بودیم)
        user_id = event.sender_id
        state = await get_state(user_id)
        
        if state != UserState.WAITING_RECEIPT:
            return

        # 2. بررسی اینکه آیا فایل ارسالی حتماً عکس است یا خیر
        if not event.photo:
            await event.respond("❌ لطفاً فقط تصویر (عکس) فیش واریزی خود را ارسال کنید.")
            return

        # 3. تغییر وضعیت کاربر در دیتابیس (برای جلوگیری از ارسال مجدد)
        await set_state(user_id, UserState.WAITING_ADMIN)
        
        # 4. آپدیت وضعیت سفارش در دیتابیس
        await update_order(user_id, {"status": "WAITING_CONFIRM"})

        # 5. اطلاع‌رسانی به کاربر
        await event.respond(
            "✅ فیش شما دریافت شد.\n"
            "مدیریت در حال بررسی است. پس از تأیید، استیکر شما ساخته و ارسال خواهد شد."
        )

        # 6. فوروارد فیش برای ادمین همراه با دکمه‌های تأیید و رد
        await bot.send_message(
            ADMIN_ID,
            f"💰 **فیش واریزی جدید**\n\n"
            f"👤 کاربر: `{user_id}`\n"
            f"🆔 نام کاربری: @{(await event.get_sender()).username or 'بدون آیدی'}",
            file=event.photo,
            buttons=[
                [Button.inline("✅ تأیید و ساخت استیکر", f"confirm_{user_id}")],
                [Button.inline("❌ رد فیش و لغو", f"cancel_{user_id}")]
            ]
        )