from telethon import events, Button
import os
from enums import UserState
from database.user_repo import set_state
from database.order_repo import get_active_order, update_order
from services.sticker_factory import build_calendar_stickers
from services.telegram_sticker_pack import create_sticker_pack 
from config import ADMIN_ID, PRODUCTS

def register(bot, sticker_client): 

    @bot.on(events.CallbackQuery)
    async def admin_action(event):
        data = event.data.decode()

        if not (data.startswith("confirm_") or data.startswith("cancel_")):
            return

        user_id = int(data.split("_")[1])
        order = get_active_order(user_id)

        if not order:
            await event.answer("❌ سفارش یافت نشد.", alert=True)
            return

        if data.startswith("confirm"):
            await event.edit("⏳ در حال رندر تصاویر و ساخت پک استیکر...")
            
            try:
                pack_info = PRODUCTS.get(order["pack"])
                if not pack_info:
                    raise ValueError(f"پک {order['pack']} تعریف نشده است.")

                template_file = os.path.join(pack_info["path"], "img1.png")
                
                images = build_calendar_stickers(
                    template_path=template_file,
                    month_name="آذر", 
                    days=30 
                )

                short_name = create_sticker_pack(
                    user_id=user_id,
                    pack_name=order["pack"],
                    images=images
                )

                if not short_name:
                    raise Exception("خطا در پاسخ سرور تلگرام برای ساخت پک.")

                sticker_link = f"https://t.me/addstickers/{short_name}"
                await bot.send_message(
                    user_id,
                    f"🎉 **پک استیکر اختصاصی شما آماده شد!**\n\n"
                    f"📦 مدل: {order['pack']}\n"
                    f"🔗 جهت افزودن به تلگرام خود، روی لینک زیر بزنید:\n\n{sticker_link}",
                    link_preview=True
                )

                update_order(user_id, {"status": "DONE", "sticker_link": sticker_link})
                set_state(user_id, UserState.START)
                
                await event.edit(f"✅ با موفقیت ساخته شد.\nلینک: {sticker_link}")

            except Exception as e:
                print(f"Admin Error: {e}")
                await event.edit(f"❌ خطای فنی:\n`{str(e)}`")

        elif data.startswith("cancel"):
            update_order(user_id, {"status": "CANCELED"})
            set_state(user_id, UserState.WAITING_RECEIPT)
            await bot.send_message(user_id, "❌ رسید شما رد شد.")
            await event.edit("❌ سفارش رد شد.")