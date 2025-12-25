import os
import jdatetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def get_persian_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def build_calendar_stickers(template_path, sticker_name, sticker_id, pack_type=1):
    rendered_images = []
    font_path = r"C:\Users\surface laptop\Desktop\python\projects\assets\fonts\Vazirmatn-Bold.ttf"
    
    output_dir = "temp_rendered"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    fa_weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
    en_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fa_months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    now = jdatetime.datetime.now()
    current_year = now.year
    current_month = now.month
    month_name = fa_months[current_month - 1]
    
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
            miladi_month_name = miladi_date.strftime("%b").upper()

            img = Image.open(template_path).convert("RGBA")
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            cx = 256 

            if pack_type == 1:
                f_brand = ImageFont.truetype(font_path, 34)    
                f_weekday = ImageFont.truetype(font_path, 28)  
                f_day_num = ImageFont.truetype(font_path, 95)   
                f_month_fa = ImageFont.truetype(font_path, 42)  
                f_month_en = ImageFont.truetype(font_path, 24)  
                f_id = ImageFont.truetype(font_path, 32)        
                draw.text((cx, 135), get_persian_text(sticker_name), font=f_brand, fill=(40, 40, 40), anchor="mm")
                draw.text((cx, 180), get_persian_text(fa_weekdays[weekday_index]), font=f_weekday, fill=(60, 60, 60), anchor="mm")
                draw.text((cx, 255), get_persian_text(day), font=f_day_num, fill=(180, 40, 40), anchor="mm")
                draw.text((cx, 325), get_persian_text(month_name), font=f_month_fa, fill=(0, 0, 0), anchor="mm")
                draw.text((cx, 370), f"{miladi_month_name} {miladi_day}", font=f_month_en, fill=(80, 80, 80), anchor="mm")
                draw.text((cx, 465), sticker_id.lower(), font=f_id, fill=(0, 0, 0), anchor="mm")

            else:
                f_brand_p2 = ImageFont.truetype(font_path, 38)
                f_medium_p2 = ImageFont.truetype(font_path, 32)
                f_id_p2 = ImageFont.truetype(font_path, 38)

                draw.text((cx, 125), get_persian_text(sticker_name), font=f_brand_p2, fill=(255, 255, 255), anchor="mm")

                draw.text((365, 235), get_persian_text(fa_weekdays[weekday_index]), font=f_medium_p2, fill=(0, 0, 0), anchor="mm")
                draw.text((145, 235), en_weekdays[weekday_index], font=f_medium_p2, fill=(60, 60, 60), anchor="mm")

                shamsi_text = f"{day} {month_name}"
                miladi_text = f"{miladi_month_name} {miladi_day}"
                draw.text((365, 315), get_persian_text(shamsi_text), font=f_medium_p2, fill=(180, 40, 40), anchor="mm")
                draw.text((145, 315), miladi_text, font=f_medium_p2, fill=(0, 0, 0), anchor="mm")

                draw.text((cx, 415), sticker_id.lower(), font=f_id_p2, fill=(0, 0, 0), anchor="mm")

            save_path = os.path.join(output_dir, f"final_{day}.png")
            img.save(save_path)
            rendered_images.append(save_path)
            
        except Exception as e:
            print(f"❌ خطا در روز {day}: {e}")

    return rendered_images