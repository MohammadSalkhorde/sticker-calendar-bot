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

    # --- ۱. ورود به پنل (هم با دستور و هم با دکمه متنی) ---
    @bot.on(events.NewMessage(from_users=ADMIN_ID))
    async def admin_entry(event):
        if event.text in ['/admin', '🛡 پنل مدیریت']:
            await set_state(ADMIN_ID, UserState.START)
            buttons = [
                [Button.inline("📊 آمار ۱۰ سفارش اخیر", data="admin_stats")],
                [Button.inline("⚙️ مدیریت پکیج‌ها", data="admin_settings")],
                [Button.inline("💳 تنظیمات کارت بانکی", data="admin_card_settings")],
                [Button.inline("📢 ارسال پیام همگانی", data="admin_broadcast")]
            ]
            await event.respond("🛡 **به پنل مدیریت خوش آمدید**\nلطفاً یکی از بخش‌های زیر را انتخاب کنید:", buttons=buttons)

    # --- ۲. مدیریت کلیک‌های دکمه‌های شیشه‌ای پنل ادمین ---
    @bot.on(events.CallbackQuery)
    async def admin_callback(event):
        if event.sender_id != ADMIN_ID: return
        data = event.data.decode()
        
        # پاسخ سریع برای جلوگیری از ارور QueryIdInvalidError
        try:
            await event.answer()
        except:
            pass

        # بخش آمار
        if data == "admin_stats":
            orders = await get_recent_orders(10)
            if not orders:
                await event.respond("📑 هنوز سفارشی ثبت نشده است.")
                return
            msg = "📑 **لیست ۱۰ سفارش اخیر:**\n\n"
            for idx, o in enumerate(orders, 1):
                user_info = f"@{o.get('username')}" if o.get('username') else f"`{o['user_id']}`"
                msg += f"{idx}. کاربر: {user_info}\n💵 مبلغ: {o.get('amount', 0):,}\n📦 پک: {o.get('pack')}\n➖➖➖➖\n"
            await event.respond(msg)

        # بخش تنظیمات پکیج‌ها
        elif data == "admin_settings":
            products = await get_products()
            msg = "⚙️ **تنظیمات پکیج‌ها:**\n\n"
            buttons = []
            for p_id, p_info in products.items():
                msg += f"📦 **{p_info['name']}**\n💰 قیمت فعلی: {p_info['price']:,} تومان\n\n"
                buttons.append([
                    Button.inline(f"💰 قیمت {p_id}", f"edit_price_{p_id}"),
                    Button.inline(f"📝 نام {p_id}", f"edit_name_{p_id}")
                ])
            buttons.append([Button.inline("🔙 بازگشت به منو", data="admin_back")])
            await event.edit(msg, buttons=buttons)

        # بخش تنظیمات کارت بانکی
        elif data == "admin_card_settings":
            card_num, card_name = await get_payment_info()
            msg = f"💳 **تنظیمات حساب بانکی:**\n\nشماره کارت: `{card_num}`\nبنام: **{card_name}**"
            buttons = [
                [Button.inline("🔢 تغییر شماره کارت", data="edit_card_number")],
                [Button.inline("📝 تغییر نام صاحب حساب", data="edit_card_name")],
                [Button.inline("🔙 بازگشت به منو", data="admin_back")]
            ]
            await event.edit(msg, buttons=buttons)

        # دکمه بازگشت
        elif data == "admin_back":
            buttons = [
                [Button.inline("📊 آمار ۱۰ سفارش اخیر", data="admin_stats")],
                [Button.inline("⚙️ مدیریت پکیج‌ها", data="admin_settings")],
                [Button.inline("💳 تنظیمات کارت بانکی", data="admin_card_settings")],
                [Button.inline("📢 ارسال پیام همگانی", data="admin_broadcast")]
            ]
            await event.edit("🛡 **پنل مدیریت ربات**", buttons=buttons)

        # شروع ویرایش‌ها
        elif data.startswith("edit_price_"):
            p_id = data.replace("edit_price_", "")
            await set_state(ADMIN_ID, f"WAIT_PRICE_{p_id}")
            await event.respond(f"🔢 قیمت جدید پکیج `{p_id}` را وارد کنید:")

        elif data.startswith("edit_name_"):
            p_id = data.replace("edit_name_", "")
            await set_state(ADMIN_ID, f"WAIT_NAME_{p_id}")
            await event.respond(f"📝 نام جدید پکیج `{p_id}` را وارد کنید:")

        elif data == "edit_card_number":
            await set_state(ADMIN_ID, "WAIT_CARD_NUMBER")
            await event.respond("💳 شماره کارت جدید را ارسال کنید:")

        elif data == "edit_card_name":
            await set_state(ADMIN_ID, "WAIT_CARD_NAME")
            await event.respond("👤 نام صاحب حساب جدید را ارسال کنید:")

        elif data == "admin_broadcast":
            await set_state(ADMIN_ID, "WAIT_BROADCAST")
            await event.respond("📢 پیامی که می‌خواهید به همه کاربران ارسال شود را بنویسید:")

        # --- بخش حساس: تایید یا رد فیش واریزی ---
        elif data.startswith("confirm_") or data.startswith("cancel_"):
            user_id = int(data.split("_")[1])
            order = await get_active_order(user_id)
            
            if not order:
                await event.respond("❌ خطای دیتابیس: سفارش فعالی برای این کاربر یافت نشد.")
                return

            if data.startswith("confirm"):
                # اطلاع رسانی به ادمین که کار شروع شده
                status_msg = await event.respond("⏳ در حال تولید و آپلود پک استیکر... لطفاً شکیبا باشید.")
                
                try:
                    products = await get_products()
                    pack_info = products.get(order["pack"])
                    p_type = 2 if "pack2" in order["pack"].lower() else 1
                    
                    assets_path = r"C:\Users\surface laptop\Desktop\python\projects\assets"
                    template_file = os.path.join(assets_path, order["pack"], "img1.png")
                    
                    # --- بخش اصلاح شده جهت ارسال نام و آیدی به کارخانه استیکر ---
                    images = build_calendar_stickers(
                        template_path=template_file, 
                        sticker_name=order.get("sticker_name", "بدون نام"), 
                        sticker_id=order.get("sticker_id", "@NoID"),
                        pack_type=p_type
                    )
                    # ---------------------------------------------------------
                    
                    # ساخت پک در تلگرام
                    short_name = create_sticker_pack(user_id=user_id, pack_name=order["pack"], images=images)
                    sticker_link = f"https://t.me/addstickers/{short_name}"
                    
                    # --- پیام جذاب نهایی برای کاربر ---
                    success_msg = (
                        "🎊 **هوراااا! استیکرهای اختصاصی شما آماده شد!** 🎊\n\n"
                        f"🎨 پکیج: **{pack_info['name']}**\n"
                        "➖➖➖➖➖➖➖➖➖➖\n"
                        "✅ پرداخت شما تایید شد و تقویم اختصاصی با موفقیت طراحی گردید.\n"
                        "همین حالا با کلیک روی لینک زیر پک خود را اضافه کنید:\n\n"
                        f"👉 [افزودن پک استیکر به تلگرام]({sticker_link})\n\n"
                        "✨ از اعتماد شما متشکریم! باز هم به ما سر بزنید."
                    )
                    await bot.send_message(user_id, success_msg, link_preview=True)

                    # بروزرسانی دیتابیس
                    user_entity = await bot.get_entity(user_id)
                    username = user_entity.username if user_entity.username else "NoID"
                    
                    await update_order(user_id, {
                        "status": "DONE", 
                        "sticker_link": sticker_link, 
                        "amount": pack_info["price"], 
                        "username": username
                    })
                    await set_state(user_id, UserState.START)
                    await status_msg.edit(f"✅ پک با موفقیت ساخته و ارسال شد:\n🔗 {sticker_link}")
                    
                except Exception as e: 
                    await event.respond(f"❌ خطا در تولید استیکر: {e}")
            
            elif data.startswith("cancel"):
                await update_order(user_id, {"status": "CANCELED"})
                await set_state(user_id, UserState.START)
                await bot.send_message(user_id, "❌ متاسفانه فیش واریزی شما توسط مدیریت تایید نشد.\nدر صورت بروز اشتباه با پشتیبانی در ارتباط باشید.")
                await event.edit("❌ فیش توسط مدیریت رد شد.")

    # --- ۳. هندلر دریافت ورودی‌های متنی ادمین ---
    @bot.on(events.NewMessage(from_users=ADMIN_ID))
    async def handle_admin_messages(event):
        if event.text.startswith('/') or event.text == '🛡 پنل مدیریت': return
        
        state = await get_state(ADMIN_ID)
        if not state: return

        if state == "WAIT_CARD_NUMBER":
            await update_payment_info(card_number=event.text)
            await event.respond(f"✅ شماره کارت به `{event.text}` تغییر یافت.")
            await set_state(ADMIN_ID, UserState.START)

        elif state == "WAIT_CARD_NAME":
            await update_payment_info(card_name=event.text)
            await event.respond(f"✅ صاحب حساب به **{event.text}** تغییر یافت.")
            await set_state(ADMIN_ID, UserState.START)

        elif state.startswith("WAIT_PRICE_"):
            p_id = state.replace("WAIT_PRICE_", "")
            if event.text.isdigit():
                await update_product_settings(p_id, new_price=int(event.text))
                await event.respond(f"✅ قیمت پک `{p_id}` بروزرسانی شد.")
                await set_state(ADMIN_ID, UserState.START)
            else:
                await event.respond("❌ خطا: قیمت باید فقط عدد باشد.")

        elif state.startswith("WAIT_NAME_"):
            p_id = state.replace("WAIT_NAME_", "")
            await update_product_settings(p_id, new_name=event.text)
            await event.respond(f"✅ نام پک `{p_id}` به **{event.text}** تغییر یافت.")
            await set_state(ADMIN_ID, UserState.START)

        elif state == "WAIT_BROADCAST":
            users = await get_all_users()
            await event.respond(f"⏳ در حال ارسال به {len(users)} نفر...")
            success = 0
            for u in users:
                try:
                    await event.client.send_message(u['user_id'], event.text)
                    success += 1
                except: continue
            await event.respond(f"✅ ارسال همگانی پایان یافت. (ارسال موفق به {success} نفر)")
            await set_state(ADMIN_ID, UserState.START)