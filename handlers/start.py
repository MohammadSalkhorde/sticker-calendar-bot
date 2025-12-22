from telethon import events, Button
from enums import UserState
from database.user_repo import set_state

def register(bot):

    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        set_state(event.sender_id, UserState.START)

        await event.respond(
            "سلام 👋\nپک مورد نظر رو انتخاب کن:",
            buttons=[
                [Button.inline("📦 پک استیکر 1", b"pack1")],
                [Button.inline("📦 پک استیکر 2", b"pack2")]
            ]
        )
