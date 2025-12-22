from database.mongo import users_col

def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

def set_state(user_id, state):
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {"state": state}},
        upsert=True
    )
