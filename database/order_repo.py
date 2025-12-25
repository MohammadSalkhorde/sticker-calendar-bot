from database.mongo import orders_col

async def create_order(user_id, pack):
    await orders_col.delete_many({"user_id": user_id, "status": {"$ne": "DONE"}})
    
    await orders_col.insert_one({
        "user_id": user_id,
        "pack": pack,
        "status": "WAITING_RECEIPT", 
        "receipt": None
    })

async def update_order(user_id, data):
    await orders_col.update_one(
        {"user_id": user_id, "status": {"$ne": "DONE"}}, 
        {"$set": data}  
    )

async def get_active_order(user_id):
    return await orders_col.find_one({"user_id": user_id, "status": {"$ne": "DONE"}})

async def get_user_orders(user_id):
    cursor = orders_col.find({"user_id": user_id, "status": "DONE"}).sort("_id", -1)
    return await cursor.to_list(length=100)

async def get_recent_orders(limit=10):
    cursor = orders_col.find({"status": "DONE"}).sort("_id", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def get_all_orders_count():
    return await orders_col.count_documents({"status": "DONE"})