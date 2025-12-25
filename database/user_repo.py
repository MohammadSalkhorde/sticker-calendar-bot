from database.mongo import users_col

def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

async def set_state(user_id, state):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"state": state}},
        upsert=True
    )

async def get_state(user_id):
    user = await users_col.find_one({"user_id": user_id})
    return user.get("state") if user else None

async def get_all_users():
    cursor = users_col.find({}, {"user_id": 1})
    return await cursor.to_list(length=None)