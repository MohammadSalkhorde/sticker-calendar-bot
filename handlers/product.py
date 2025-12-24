from telethon import events
from database.order_repo import create_order
from database.settings_repo import get_products, get_payment_info
from enums import UserState
from database.user_repo import set_state

def register(bot):
    @bot.on(events.CallbackQuery)
    async def product_click(event):
        data = event.data.decode()
        products = await get_products()
        card_num, card_name = await get_payment_info()
        
        if data in products:
            selected = products[data]
            await create_order(event.sender_id, data)
            await set_state(event.sender_id, UserState.WAITING_RECEIPT)
            
            caption = (
                f"✅ پکیج انتخاب شده: **{selected['name']}**\n\n"
                f"💰 مبلغ قابل پرداخت: **{selected['price']:,} تومان**\n"
                f"💳 شماره کارت: `{card_num}`\n"
                f"👤 بنام: **{card_name}**\n\n"
                "لطفاً پس از واریز، تصویر فیش را ارسال کنید."
            )
            await event.respond(caption)