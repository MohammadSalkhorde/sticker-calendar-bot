from PIL import Image, ImageDraw, ImageFont
import os

def render_text(template_file, text, output_path):
    img = Image.open(template_file).convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("ARIAL.TTF", 80) 
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((img.width - w)/2, (img.height - h)/2), text, font=font, fill=(0,0,0,255))

    img.save(output_path, "PNG")