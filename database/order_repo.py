from database.mongo import orders_col

def create_order(user_id, pack):
    orders_col.delete_many({"user_id": user_id, "status": {"$ne": "DONE"}})
    
    orders_col.insert_one({
        "user_id": user_id,
        "pack": pack,
        "status": "WAITING_RECEIPT", 
        "receipt": None
    })

def update_order(user_id, data):
    orders_col.update_one(
        {"user_id": user_id, "status": {"$ne": "DONE"}}, 
        {"$set": data}  
    )

def get_active_order(user_id):
    return orders_col.find_one({"user_id": user_id, "status": {"$ne": "DONE"}})