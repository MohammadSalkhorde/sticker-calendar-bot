from telethon import events, Button
import os
from database.settings_repo import get_products, get_payment_info
from database.order_repo import create_order, update_order
from database.user_repo import set_state, get_state
from enums import UserState

def register(bot):
    # ۱. نمایش لیست پکیج‌ها
    @bot.on(events.NewMessage(pattern="🎨 ساخت استیکر"))
    async def show_packs(event):
        products = await get_products()
        assets_path = r"C:\Users\surface laptop\Desktop\python\projects\assets"
        await event.respond("✨ در حال بارگذاری پکیج‌های فعال...")

        for p_id, p_info in products.items():
            photo_path = os.path.join(assets_path, p_id, "img1.png")
            caption = (
                f"📦 **پکیج: {p_info['name']}**\n"
                f"💰 قیمت: {p_info['price']:,} تومان\n\n"
                f"📅 این پکیج شامل تقویم کامل ماه جاری با طراحی اختصاصی است."
            )
            buttons = [Button.inline(f"💎 انتخاب {p_info['name']}", f"select_{p_id}")]

            if os.path.exists(photo_path):
                await event.client.send_file(event.chat_id, photo_path, caption=caption, buttons=buttons)
            else:
                await event.respond(f"⚠️ عکس قالب پیدا نشد!\n\n{caption}", buttons=buttons)

    # ۲. مرحله شروع دریافت اطلاعات (بعد از کلیک روی انتخاب پک)
    @bot.on(events.CallbackQuery(pattern=r"select_"))
    async def start_info_collection(event):
        p_id = event.data.decode().split("_")[1]
        # ایجاد سفارش اولیه
        await create_order(event.sender_id, p_id)
        # تغییر وضعیت به انتظار برای دریافت نام
        await set_state(event.sender_id, UserState.WAITING_NAME)
        
        await event.delete()
        await event.respond(
            "✍️ **مرحله اول:**\n\n"
            "لطفاً نام مستعار، نام برند یا اسمی که می‌خواهید روی تمامی استیکرها درج شود را ارسال کنید:"
        )

    # ۳. هندلر دریافت نام و آیدی (متنی)
    @bot.on(events.NewMessage)
    async def collect_text_info(event):
        if event.text.startswith('/') or event.text in ["🎨 ساخت استیکر", "📂 استیکرهای ساخته شده", "📞 پشتیبانی", "❓ راهنما", "🛡 پنل مدیریت"]:
            return

        state = await get_state(event.sender_id)
        
        # دریافت نام
        if state == UserState.WAITING_NAME:
            sticker_name = event.text
            await update_order(event.sender_id, {"sticker_name": sticker_name})
            await set_state(event.sender_id, UserState.WAITING_ID_STENCIL)
            await event.respond(
                f"✅ نام **{sticker_name}** ثبت شد.\n\n"
                "🔗 **مرحله دوم:**\n"
                "حالا آیدی تلگرام یا اینستاگرام خود را جهت درج در استیکر به صورت `@ID` ارسال کنید:"
            )

        # دریافت آیدی
        elif state == UserState.WAITING_ID_STENCIL:
            if not event.text.startswith("@"):
                await event.respond("⚠️ لطفا آیدی را حتماً با @ شروع کنید (مثال: @YourID):")
                return
            
            sticker_id = event.text
            await update_order(event.sender_id, {"sticker_id": sticker_id})
            await set_state(event.sender_id, UserState.WAITING_RECEIPT)
            
            # نمایش مرحله پرداخت
            from database.order_repo import get_active_order
            order = await get_active_order(event.sender_id)
            products = await get_products()
            selected_pack = products.get(order['pack'])
            card_num, card_name = await get_payment_info()
            
            pay_caption = (
                f"🛍 **سفارش شما در مرحله نهایی**\n\n"
                f"📦 پکیج: **{selected_pack['name']}**\n"
                f"🏷 نام درج شونده: **{order['sticker_name']}**\n"
                f"🔗 آیدی درج شونده: **{order['sticker_id']}**\n"
                f"💰 مبلغ قابل واریز: **{selected_pack['price']:,} تومان**\n\n"
                f"💳 شماره کارت: `{card_num}`\n"
                f"👤 بنام: **{card_name}**\n\n"
                "👇 لطفاً پس از واریز، تصویر فیش خود را همین‌جا ارسال کنید."
            )
            
            assets_path = r"C:\Users\surface laptop\Desktop\python\projects\assets"
            photo_path = os.path.join(assets_path, order['pack'], "img1.png")
            
            if os.path.exists(photo_path):
                await event.client.send_file(event.chat_id, photo_path, caption=pay_caption)
            else:
                await event.respond(pay_caption)