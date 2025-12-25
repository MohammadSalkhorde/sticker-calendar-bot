from telethon import events, Button
from enums import UserState
from database.user_repo import set_state, get_state
from database.order_repo import get_active_order
from config import ADMIN_ID

def register(bot):
    @bot.on(events.NewMessage(func=lambda e: e.photo))
    async def receipt_handler(event):
        state = await get_state(event.sender_id)
        if state == UserState.WAITING_RECEIPT:
            await set_state(event.sender_id, f"CONFIRM_RECEIPT_{event.message.id}")
            
            buttons = [
                [Button.inline("✅ بله، مطمئنم و ارسال شود", data="final_confirm_receipt")],
                [Button.inline("❌ خیر، ارسال نشود", data="cancel_receipt")]
            ]
            
            await event.respond(
                "📸 **تصویر فیش شما دریافت شد.**\n"
                "آیا از صحت تصویر و مبلغ واریزی اطمینان دارید؟ در صورت تایید، فیش برای مدیریت ارسال خواهد شد.",
                buttons=buttons
            )

    @bot.on(events.CallbackQuery)
    async def receipt_callback(event):
        data = event.data.decode()
        state = await get_state(event.sender_id)

        if data == "final_confirm_receipt" and str(state).startswith("CONFIRM_RECEIPT_"):
            try:
                msg_id = int(state.split("_")[-1])
                
                source_msg = await event.client.get_messages(event.chat_id, ids=msg_id)
                
                if not source_msg or not source_msg.photo:
                    await event.respond("❌ خطایی رخ داد: عکس فیش یافت نشد. لطفاً دوباره ارسال کنید.")
                    return

                order = await get_active_order(event.sender_id)
                sticker_name = order.get('sticker_name', 'نامشخص')
                sticker_id = order.get('sticker_id', 'نامشخص')
                pack_name = order.get('pack', 'نامشخص')

                admin_caption = (
                    f"👤 **فیش جدید واریزی دریافت شد!**\n\n"
                    f"🆔 آیدی عددی: `{event.sender_id}`\n"
                    f"🏷 نام درخواستی: **{sticker_name}**\n"
                    f"🔗 آیدی درخواستی: **{sticker_id}**\n"
                    f"📦 پکیج انتخاب شده: **{pack_name}**\n"
                    f"➖➖➖➖➖➖➖➖"
                )
                
                buttons = [
                    [Button.inline("✅ تایید و ساخت استیکر", data=f"confirm_{event.sender_id}")],
                    [Button.inline("❌ رد فیش", data=f"cancel_{event.sender_id}")]
                ]

                await event.client.send_file(
                    ADMIN_ID,
                    file=source_msg.photo, 
                    caption=admin_caption,
                    buttons=buttons
                )
                
                await set_state(event.sender_id, UserState.WAITING_APPROVAL)
                await event.edit("🚀 **فیش شما با موفقیت برای مدیریت ارسال شد.**\nمنتظر تایید و ساخت استیکر بمانید.")

            except Exception as e:
                print(f"Error in receipt_callback: {e}")
                await event.respond("❌ خطایی در ارسال فیش رخ داد. لطفاً دوباره تلاش کنید.")

        elif data == "cancel_receipt":
            await set_state(event.sender_id, UserState.WAITING_RECEIPT)
            await event.edit("❌ ارسال فیش لغو شد. می‌توانید تصویر جدیدی ارسال کنید.")