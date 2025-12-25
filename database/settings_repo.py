from database.mongo import settings_col

async def get_products():
    doc = await settings_col.find_one({"type": "products_config"})
    if doc:
        return doc.get("products", {})
    
    return {
        "pack1": {"price": 50000, "name": "پک استیکر ۱"},
        "pack2": {"price": 80000, "name": "پک استیکر ۲"}
    }

async def get_payment_info():
    doc = await settings_col.find_one({"type": "payment_config"})
    if doc:
        return doc.get("card_number", "0000-0000-0000-0000"), doc.get("card_name", "ثبت نشده")
    return "0000-0000-0000-0000", "ثبت نشده"

async def update_payment_info(card_number=None, card_name=None):
    data = {}
    if card_number: data["card_number"] = card_number
    if card_name: data["card_name"] = card_name
    
    await settings_col.update_one(
        {"type": "payment_config"},
        {"$set": data},
        upsert=True
    )

async def update_product_settings(pack_id, new_price=None, new_name=None):
    products = await get_products()
    if pack_id in products:
        if new_price is not None: products[pack_id]["price"] = int(new_price)
        if new_name is not None: products[pack_id]["name"] = new_name
            
        await settings_col.update_one(
            {"type": "products_config"},
            {"$set": {"products": products}},
            upsert=True
        )