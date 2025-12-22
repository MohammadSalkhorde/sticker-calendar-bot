from telethon import events
from config import PRODUCTS, CARD_NUMBER
from database.order_repo import create_order
from database.user_repo import set_state
from enums import UserState

def register(bot):

    @bot.on(events.CallbackQuery(data=b"pack1"))
    @bot.on(events.CallbackQuery(data=b"pack2"))
    async def product(event):
        pack = event.data.decode()
        price = PRODUCTS[pack]["price"]

        create_order(event.sender_id, pack)
        set_state(event.sender_id, UserState.WAITING_RECEIPT)

        await event.edit(
            f"💳 مبلغ: {price:,} تومان\n"
            f"شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید رو بفرست"
        )
