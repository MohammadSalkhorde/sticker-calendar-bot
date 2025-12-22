import os
from telethon.network.connection.tcpmtproxy import ConnectionTcpMTProxyAbridged

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_ID = 2952632
API_HASH = "f471be4609e8ad788bffc6aaa8648942"
BOT_TOKEN = "8405171144:AAF18BIJ-h_zZ7jj6w_5yeFjNsrpn8qubFc"

ADMIN_ID = 6802129018
CARD_NUMBER = "1234-5678-9012-3456"

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "sticker_bot"


PROXY = dict(
    connection=ConnectionTcpMTProxyAbridged,
    proxy=("full.siteliveim.co.uk", 443, "dd104462821249bd7ac519130220c25d09")
)


PRODUCTS = {
    "pack1": {
        "price": 50000,
        "path": os.path.join(BASE_DIR, "assets", "pack1")
    },
    "pack2": {
        "price": 80000,
        "path": os.path.join(BASE_DIR, "assets", "pack2")
    }
}
