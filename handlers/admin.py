from telethon import events, Button
import os
from enums import UserState
from database.user_repo import set_state, get_all_users, get_state
from database.order_repo import get_active_order, update_order, get_recent_orders
from database.settings_repo import get_products, update_product_settings, get_payment_info, update_payment_info
from services.sticker_factory import build_calendar_stickers
from services.telegram_sticker_pack import create_sticker_pack 
from config import ADMIN_ID

def register(bot, sticker_client): 

    @bot.on(events.NewMessage(pattern='/admin', from_users=ADMIN_ID))
    async def admin_panel(event):
        await set_state(ADMIN_ID, UserState.START)
        buttons = [
            [Button.inline("📊 آمار ۱۰ سفارش اخیر", data="admin_stats")],
            [Button.inline("⚙️ مدیریت پکیج‌ها", data="admin_settings")],
            [Button.inline("💳 تنظیمات کارت بانکی", data="admin_card_settings")],
            [Button.inline("📢 ارسال پیام همگانی", data="admin_broadcast")]
        ]
        await event.respond("🛡 **پنل مدیریت ربات**", buttons=buttons)

    @bot.on(events.CallbackQuery)
    async def admin_callback(event):
        if event.sender_id != ADMIN_ID: return
        data = event.data.decode()
        
        if data == "admin_stats":
            orders = await get_recent_orders(10)
            msg = "📑 **لیست ۱۰ سفارش اخیر:**\n\n"
            for idx, o in enumerate(orders, 1):
                user_info = f"@{o.get('username')}" if o.get('username') else f"`{o['user_id']}`"
                msg += f"{idx}. کاربر: {user_info}\n💵 مبلغ: {o.get('amount', 0):,}\n📦 پک: {o.get('pack')}\n➖➖➖➖\n"
            await event.respond(msg)

        elif data == "admin_settings":
            products = await get_products()
            msg = "⚙️ **تنظیمات پکیج‌ها:**\n\n"
            buttons = []
            for p_id, p_info in products.items():
                msg += f"📦 **{p_info['name']}**\n💰 قیمت: {p_info['price']:,}\n\n"
                buttons.append([Button.inline(f"💰 قیمت {p_id}", f"edit_price_{p_id}"), Button.inline(f"📝 نام {p_id}", f"edit_name_{p_id}")])
            buttons.append([Button.inline("🔙 بازگشت", data="admin_back")])
            await event.edit(msg, buttons=buttons)

        elif data == "admin_card_settings":
            card_num, card_name = await get_payment_info()
            msg = f"💳 **تنظیمات پرداخت:**\n\nشماره کارت: `{card_num}`\nبنام: **{card_name}**"
            buttons = [
                [Button.inline("🔢 تغییر شماره کارت", data="edit_card_number")],
                [Button.inline("📝 تغییر نام صاحب حساب", data="edit_card_name")],
                [Button.inline("🔙 بازگشت", data="admin_back")]
            ]
            await event.edit(msg, buttons=buttons)

        elif data == "admin_back":
            buttons = [[Button.inline("📊 آمار", data="admin_stats")], [Button.inline("⚙️ تنظیمات", data="admin_settings")], [Button.inline("💳 کارت بانکی", data="admin_card_settings")], [Button.inline("📢 همگانی", data="admin_broadcast")]]
            await event.edit("🛡 **پنل مدیریت**", buttons=buttons)

        elif data.startswith("edit_price_"):
            p_id = data.replace("edit_price_", "")
            await set_state(ADMIN_ID, f"WAIT_PRICE_{p_id}")
            await event.respond("لطفاً قیمت جدید را بفرستید:")

        elif data.startswith("edit_name_"):
            p_id = data.replace("edit_name_", "")
            await set_state(ADMIN_ID, f"WAIT_NAME_{p_id}")
            await event.respond("لطفاً نام جدید را بفرستید:")

        elif data == "edit_card_number":
            await set_state(ADMIN_ID, "WAIT_CARD_NUMBER")
            await event.respond("لطفاً شماره کارت جدید را بفرستید:")

        elif data == "edit_card_name":
            await set_state(ADMIN_ID, "WAIT_CARD_NAME")
            await event.respond("لطفاً نام صاحب حساب را بفرستید:")

        elif data.startswith("confirm_") or data.startswith("cancel_"):
            user_id = int(data.split("_")[1])
            order = await get_active_order(user_id)
            if data.startswith("confirm") and order:
                await event.edit("⏳ در حال تولید استیکر و آپلود در تلگرام... لطفاً کمی صبر کنید.")
                try:
                    products = await get_products()
                    pack_info = products.get(order["pack"])
                    p_type = 2 if "pack2" in order["pack"].lower() else 1
                    
                    assets_path = r"C:\Users\surface laptop\Desktop\python\projects\assets"
                    template_file = os.path.join(assets_path, order["pack"], "img1.png")
                    
                    # تولید تصاویر
                    images = build_calendar_stickers(template_path=template_file, pack_type=p_type)
                    
                    # ساخت پک در تلگرام
                    short_name = create_sticker_pack(user_id=user_id, pack_name=order["pack"], images=images)
                    sticker_link = f"https://t.me/addstickers/{short_name}"
                    
                    # --- تغییر متن پیام طبق درخواست شما ---
                    success_msg = (
                        "🎉 فیش شما تایید شد!\n"
                        "✅ لینک پک استیکر شما:\n"
                        f"{sticker_link}"
                    )
                    await bot.send_message(user_id, success_msg)
                    # -------------------------------------

                    await update_order(user_id, {
                        "status": "DONE", 
                        "sticker_link": sticker_link, 
                        "amount": pack_info["price"], 
                        "username": (await bot.get_entity(user_id)).username
                    })
                    await set_state(user_id, UserState.START)
                    await event.edit(f"✅ با موفقیت برای کاربر ارسال شد:\n{sticker_link}")
                    
                except Exception as e: 
                    await event.respond(f"❌ خطا در فرآیند ساخت: {e}")
            
            elif data.startswith("cancel"):
                await update_order(user_id, {"status": "CANCELED"})
                await set_state(user_id, UserState.START)
                await bot.send_message(user_id, "❌ متاسفانه فیش واریزی شما توسط مدیریت رد شد.")
                await event.edit("❌ فیش رد و به کاربر اطلاع داده شد.")

    @bot.on(events.NewMessage(from_users=ADMIN_ID))
    async def handle_admin_messages(event):
        if event.text.startswith('/'): return
        state = await get_state(ADMIN_ID)
        if state == "WAIT_CARD_NUMBER":
            await update_payment_info(card_number=event.text)
            await event.respond("✅ شماره کارت آپدیت شد.")
            await set_state(ADMIN_ID, UserState.START)
        elif state == "WAIT_CARD_NAME":
            await update_payment_info(card_name=event.text)
            await event.respond("✅ نام صاحب حساب آپدیت شد.")
            await set_state(ADMIN_ID, UserState.START)
        elif state.startswith("WAIT_PRICE_"):
            p_id = state.replace("WAIT_PRICE_", "")
            await update_product_settings(p_id, new_price=event.text)
            await event.respond("✅ قیمت آپدیت شد.")
            await set_state(ADMIN_ID, UserState.START)
        elif state.startswith("WAIT_NAME_"):
            p_id = state.replace("WAIT_NAME_", "")
            await update_product_settings(p_id, new_name=event.text)
            await event.respond("✅ نام آپدیت شد.")
            await set_state(ADMIN_ID, UserState.START)