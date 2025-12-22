from telethon import events, Button
from enums import UserState
from database.user_repo import set_state
from database.order_repo import get_active_order, update_order
from services.sticker_factory import build_calendar_stickers
from services.telegram_sticker_pack import create_sticker_pack
from config import ADMIN_ID, PRODUCTS

def register(bot, sticker_client):  # ✅ MTProto client هم میاد

    @bot.on(events.CallbackQuery)
    async def admin_action(event):
        data = event.data.decode()

        if not (data.startswith("confirm_") or data.startswith("cancel_")):
            return

        user_id = int(data.split("_")[1])
        order = get_active_order(user_id)

        if not order:
            await event.edit("❌ سفارش پیدا نشد")
            return

        if data.startswith("confirm"):
            # ساخت تصاویر تقویم
            images = build_calendar_stickers(
                PRODUCTS[order["pack"]]["path"],
                month_name="آذر",
                days=30
            )

            # ساخت پک استیکر با MTProto
            short_name = await create_sticker_pack(
                sticker_client,
                user_id=ADMIN_ID,  # اکانت واقعی که پک می‌سازد
                pack_name=order["pack"],
                images=images
            )

            # ارسال لینک یا نام کوتاه پک به کاربر
            await bot.send_message(
                user_id,
                f"🎉 پک استیکر شما ساخته شد!\nنام کوتاه پک: {short_name}"
            )
            update_order(user_id, {"status": "DONE"})
            await event.edit("✅ تایید شد")

        else:
            await bot.send_message(user_id, "❌ سفارش لغو شد")
            update_order(user_id, {"status": "CANCELED"})
            await event.edit("❌ لغو شد")
