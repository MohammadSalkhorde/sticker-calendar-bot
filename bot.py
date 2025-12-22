from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, PROXY
from handlers import start, product, receipt, admin

# Bot API client با پروکسی
bot = TelegramClient("bot_session", API_ID, API_HASH, **PROXY).start(bot_token=BOT_TOKEN)

# MTProto client با پروکسی
sticker_client = TelegramClient("sticker_session", API_ID, API_HASH, **PROXY)

# register handlers
start.register(bot)
product.register(bot)
receipt.register(bot)
admin.register(bot, sticker_client)

print("🤖 Bot is running...")

with bot:
    sticker_client.start()
    bot.run_until_disconnected()
