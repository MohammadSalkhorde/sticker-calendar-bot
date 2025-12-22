from PIL import Image, ImageDraw, ImageFont

def render_text(template_file, text, output_path):
    img = Image.open(template_file).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 40)

    # اندازه متن با textbbox
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # متن را وسط تصویر قرار بده
    draw.text(((img.width - w)/2, (img.height - h)/2), text, font=font, fill=(255,255,255,255))

    img.save(output_path, "WEBP")
