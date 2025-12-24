from database.mongo import users_col

def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

# اضافه کردن کلمه async به ابتدای تابع
async def set_state(user_id, state):
    # اضافه کردن await قبل از دستور دیتابیس
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"state": state}},
        upsert=True
    )

async def get_state(user_id):
    # اضافه کردن await برای گرفتن نتیجه واقعی
    user = await users_col.find_one({"user_id": user_id})
    return user.get("state") if user else None

async def get_all_users():
    # در موتور برای گرفتن لیست باید از to_list استفاده کرد یا await روی خود کوئری
    cursor = users_col.find({}, {"user_id": 1})
    return await cursor.to_list(length=None)