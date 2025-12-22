import os
from services.image_renderer import render_text

def build_calendar_stickers(template_path, month_name, days):
    output_dir = os.path.join(template_path, "output")
    os.makedirs(output_dir, exist_ok=True)

    # پیدا کردن فایل‌های تصویر داخل فولدر
    templates = [os.path.join(template_path, f) 
                 for f in os.listdir(template_path) 
                 if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    images = []
    for day in range(1, days+1):
        # می‌تونی از اولین تصویر به عنوان تمپلیت استفاده کنی
        template_file = templates[0]
        output_path = os.path.join(output_dir, f"{day}.webp")
        render_text(template_file, str(day), output_path)
        images.append(output_path)
    return images
