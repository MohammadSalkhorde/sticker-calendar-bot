from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME

# ایجاد کلاینت به صورت غیرهمزمان
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# کالکشن‌ها
users_col = db["users"]
orders_col = db["orders"]
settings_col = db["settings"]