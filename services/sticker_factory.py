import os
import jdatetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def get_persian_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def build_calendar_stickers(template_path, month_name, days=30):
    rendered_images = []
    font_path = r"C:\Users\surface laptop\Desktop\python\projects\assets\fonts\Vazirmatn-Bold.ttf"
    
    output_dir = "temp_rendered"
    os.makedirs(output_dir, exist_ok=True)

    fa_weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
    en_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in range(1, days + 1):
        try:
            date_obj = jdatetime.datetime(1404, 9, day) 
            weekday_index = date_obj.weekday()
            day_name_fa = fa_weekdays[weekday_index]
            day_name_en = en_weekdays[weekday_index]

            img = Image.open(template_path).convert("RGBA")
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            if os.path.exists(font_path):
                font_main = ImageFont.truetype(font_path, 80)   
                font_sub = ImageFont.truetype(font_path, 35)    
                font_tiny = ImageFont.truetype(font_path, 25)   
            else:
                raise FileNotFoundError("فونت پیدا نشد!")

            center_x = 256
            center_y = 280

            draw.text((center_x + 60, center_y - 120), get_persian_text(day_name_fa), font=font_sub, fill=(50, 50, 50), anchor="mm")
            draw.text((center_x - 60, center_y - 120), day_name_en, font=font_sub, fill=(50, 50, 50), anchor="mm")

            draw.text((center_x, center_y - 80), get_persian_text("۱۴۰۴ - 2025"), font=font_tiny, fill=(100, 100, 100), anchor="mm")

            draw.text((center_x + 70, center_y - 20), get_persian_text(month_name), font=font_sub, fill=(0, 0, 0), anchor="mm")
            draw.text((center_x - 70, center_y - 20), "Dec", font=font_sub, fill=(0, 0, 0), anchor="mm")

            draw.text((center_x + 70, center_y + 60), get_persian_text(day), font=font_main, fill=(139, 43, 22), anchor="mm")
            draw.text((center_x - 70, center_y + 60), str(day).zfill(2), font=font_main, fill=(139, 43, 22), anchor="mm")

            save_path = os.path.join(output_dir, f"final_{day}.png")
            img.save(save_path)
            rendered_images.append(save_path)
            
        except Exception as e:
            print(f"❌ خطا در روز {day}: {e}")

    return rendered_images