import os
import jdatetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def get_persian_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def build_calendar_stickers(template_path, pack_type=1):
    rendered_images = []
    # مسیر فونت را حتما چک کنید
    font_path = r"C:\Users\surface laptop\Desktop\python\projects\assets\fonts\Vazirmatn-Bold.ttf"
    
    output_dir = "temp_rendered"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    fa_weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
    en_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fa_months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    # دریافت تاریخ فعلی شمسی
    now = jdatetime.datetime.now()
    current_year = now.year
    current_month = now.month
    month_name = fa_months[current_month - 1]
    
    # محاسبه تعداد روزهای ماه
    if current_month <= 6:
        days_in_month = 31
    elif current_month <= 11:
        days_in_month = 30
    else:
        days_in_month = 29 if not now.is_leap() else 30

    for day in range(1, days_in_month + 1):
        try:
            shamsi_date = jdatetime.date(current_year, current_month, day)
            weekday_index = shamsi_date.weekday()
            miladi_date = shamsi_date.togregorian()
            miladi_day = miladi_date.strftime("%d")
            miladi_month_name = miladi_date.strftime("%b")
            miladi_year = miladi_date.year

            # باز کردن قالب
            img = Image.open(template_path).convert("RGBA")
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            if not os.path.exists(font_path):
                raise FileNotFoundError(f"فونت در مسیر {font_path} یافت نشد!")

            if pack_type == 1:
                # --- چیدمان متمرکز در دایره (پک 1) ---
                f_main = ImageFont.truetype(font_path, 85)
                f_sub = ImageFont.truetype(font_path, 32)
                cx, cy = 256, 256
                
                draw.text((cx + 55, cy - 85), get_persian_text(fa_weekdays[weekday_index]), font=f_sub, fill=(50, 50, 50), anchor="mm")
                draw.text((cx - 55, cy - 85), en_weekdays[weekday_index], font=f_sub, fill=(50, 50, 50), anchor="mm")
                draw.text((cx, cy - 50), get_persian_text(f"{current_year} - {miladi_year}"), font=f_sub, fill=(100, 100, 100), anchor="mm")
                draw.text((cx + 65, cy), get_persian_text(month_name), font=f_sub, fill=(0, 0, 0), anchor="mm")
                draw.text((cx - 65, cy), miladi_month_name, font=f_sub, fill=(0, 0, 0), anchor="mm")
                draw.text((cx + 65, cy + 70), get_persian_text(day), font=f_main, fill=(139, 43, 22), anchor="mm")
                draw.text((cx - 65, cy + 70), miladi_day, font=f_main, fill=(139, 43, 22), anchor="mm")

            else:
                # --- چیدمان جدول‌بندی شده و ستونی (پک 2) ---
                # تنظیم سایز فونت‌ها برای جلوگیری از تداخل
                f_day = ImageFont.truetype(font_path, 90)    # عدد روز
                f_month = ImageFont.truetype(font_path, 38)  # نام ماه
                f_header = ImageFont.truetype(font_path, 28) # روز هفته و سال (سایز کوچک‌تر شد)
                
                # تعریف ستون‌های مجازی برای تراز دقیق (عرض کل 512 است)
                col_right = 395  # مرکز بخش راست (فارسی)
                col_center = 256 # مرکز کل تصویر (سال‌ها)
                col_left = 117   # مرکز بخش چپ (انگلیسی)
                
                # --- ردیف هدر (بخش رنگی بالای تقویم) ---
                # روز هفته فارسی
                draw.text((col_right, 50), get_persian_text(fa_weekdays[weekday_index]), font=f_header, fill="white", anchor="mm")
                # سال‌ها (زیر هم در مرکز)
                draw.text((col_center, 40), get_persian_text(str(current_year)), font=f_header, fill="white", anchor="mm")
                draw.text((col_center, 78), str(miladi_year), font=f_header, fill="white", anchor="mm")
                # روز هفته انگلیسی
                draw.text((col_left, 50), en_weekdays[weekday_index], font=f_header, fill="white", anchor="mm")
                
                # --- بخش بدنه (بخش سفید پایین تقویم) ---
                y_month = 345 # ارتفاع نام ماه
                y_day = 430   # ارتفاع عدد روز
                
                # ستون راست: شمسی
                draw.text((col_right, y_month), get_persian_text(month_name), font=f_month, fill=(0, 0, 0), anchor="mm")
                draw.text((col_right, y_day), get_persian_text(day), font=f_day, fill=(139, 43, 22), anchor="mm")
                
                # ستون چپ: میلادی
                draw.text((col_left, y_month), miladi_month_name, font=f_month, fill=(0, 0, 0), anchor="mm")
                draw.text((col_left, y_day), miladi_day, font=f_day, fill=(139, 43, 22), anchor="mm")

            # ذخیره فایل نهایی
            save_path = os.path.join(output_dir, f"final_{day}.png")
            img.save(save_path)
            rendered_images.append(save_path)
            
        except Exception as e:
            print(f"❌ خطا در رندر روز {day}: {e}")

    return rendered_images