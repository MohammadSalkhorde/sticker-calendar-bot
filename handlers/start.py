from telethon import events, Button
from enums import UserState
from database.user_repo import set_state
from database.order_repo import get_user_orders 
from config import ADMIN_ID

def register(bot):
    @bot.on(events.NewMessage(pattern="/start"))
    async def start_handler(event):
        await set_state(event.sender_id, UserState.START)
        
        buttons = [
            [Button.text("🎨 ساخت استیکر", resize=True)],
            [Button.text("📂 استیکرهای ساخته شده"), Button.text("📞 پشتیبانی")],
            [Button.text("❓ راهنما")]
        ]
        
        if event.sender_id == ADMIN_ID:
            buttons.append([Button.text("🛡 پنل مدیریت")])

        welcome_text = (
            "سلام خوش آمدید! ✨\n\n"
            "با این ربات می‌توانید تقویم ماه جاری را روی استیکرهای خودتان داشته باشید.\n"
            "لطفاً از منوی زیر یک گزینه را انتخاب کنید:"
        )
        
        await event.respond(welcome_text, buttons=buttons)

    @bot.on(events.NewMessage(pattern="📂 استیکرهای ساخته شده"))
    async def my_stickers_handler(event):
        user_id = event.sender_id
        
        all_orders = await get_user_orders(user_id)
        
        completed = [o for o in all_orders if o.get('status') == 'DONE']
        
        if not completed:
            await event.respond(
                "📉 **شما هنوز هیچ پکیج استیکری ثبت نکرده‌اید.**\n\n"
                "همین حالا با زدن دکمه '🎨 ساخت استیکر' اولین پک خود را سفارش دهید!"
            )
            return

        msg = "📂 **آرشیو استیکرهای اختصاصی شما**\n"
        msg += "➖➖➖➖➖➖➖➖➖➖\n\n"
        
        for idx, order in enumerate(completed, 1):
            pack_id = order.get('pack', 'نامشخص')
            link = order.get('sticker_link', '#')
            
            msg += f"{idx}️⃣ **پکیج:** `{pack_id}`\n"
            msg += f"🔗 **لینک نصب:** [کلیک کنید برای افزودن]({link})\n"
            msg += "────────────────────\n"

        await event.respond(msg, link_preview=False)

    @bot.on(events.NewMessage(pattern="❓ راهنما"))
    async def help_handler(event):
        help_text = (
            "🚀 **چطور استیکر بسازم؟**\n\n"
            "1️⃣ دکمه '🎨 ساخت استیکر' را بزنید.\n"
            "2️⃣ پکیج مورد نظر را انتخاب کرده و مبلغ را واریز کنید.\n"
            "3️⃣ عکس فیش را ارسال و تایید کنید.\n"
            "4️⃣ ربات تقویم را روی قالب شما ست کرده و لینک پک را برایتان می‌فرستد."
        )
        await event.respond(help_text)

    @bot.on(events.NewMessage(pattern="📞 پشتیبانی"))
    async def support_handler(event):
        await event.respond(
            "👤 **پشتیبانی مستقیم**\n\n"
            "در صورت بروز هرگونه مشکل یا سوال با آیدی زیر در ارتباط باشید:\n"
            "👉 @Your_Admin_ID"
        )