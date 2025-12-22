from telethon import TelegramClient
from config import API_ID, API_HASH

sticker_client = TelegramClient("sticker_user", API_ID, API_HASH)

async def start_sticker_client():
    await sticker_client.start()
