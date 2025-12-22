# handlers/receipt.py
from telethon import events, Button
from enums import UserState
from database.user_repo import get_user, set_state
from database.order_repo import get_active_order, update_order
from config import ADMIN_ID
from telethon.tl.types import InputPeerUser

def register(bot):
    # دریافت عکس رسید
    @bot.on(events.NewMessage)
    async def receipt(event):
        user = get_user(event.sender_id)
        if not user or user["state"] != UserState.WAITING_RECEIPT:
            return

        if not event.photo:
            await event.reply("❌ فقط عکس رسید ارسال کن")
            return

        # دانلود و ذخیره رسید
        file_path = await event.download_media()
        update_order(event.sender_id, {"receipt": file_path, "status": "checking"})
        set_state(event.sender_id, UserState.CONFIRM_RECEIPT)

        # دکمه‌ها با شناسه کاربر
        await event.reply(
            "آیا از ارسال رسید به پشتیبانی اطمینان دارید؟",
            buttons=[
                [
                    Button.inline("✅ تایید", f"send_admin_{event.sender_id}"),
                    Button.inline("❌ لغو", f"cancel_send_{event.sender_id}")
                ]
            ]
        )

    # لغو ارسال رسید
    @bot.on(events.CallbackQuery)
    async def cancel_send(event):
        data = event.data.decode()
        if not data.startswith("cancel_send_"):
            return

        user_id = int(data.split("_")[2])
        set_state(user_id, UserState.WAITING_RECEIPT)
        await event.edit("❌ ارسال رسید لغو شد. لطفا دوباره عکس ارسال کنید.")

    # ارسال رسید به ادمین
    @bot.on(events.CallbackQuery)
    async def send_admin(event):
        data = event.data.decode()
        if not data.startswith("send_admin_"):
            return

        user_id = int(data.split("_")[2])
        order = get_active_order(user_id)
        if not order or "receipt" not in order:
            await event.edit("❌ رسید پیدا نشد")
            return

        # ارسال فایل رسید به ادمین
        await bot.send_file(
            ADMIN_ID,
            order["receipt"],
            caption=f"🧾 رسید کاربر: {user_id}",
            buttons=[
                [
                    Button.inline(f"✅ تایید پرداخت {user_id}", f"confirm_{user_id}"),
                    Button.inline(f"❌ لغو پرداخت {user_id}", f"cancel_{user_id}")
                ]
            ]
        )

        set_state(user_id, UserState.WAITING_ADMIN)
        await event.edit("رسید برای پشتیبانی ارسال شد")
