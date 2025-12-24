import os
import random
import string
import requests
import json
from PIL import Image 
from config import BOT_TOKEN

def create_sticker_pack(user_id, pack_name, images):
    bot_username = "sticker_saz5_bot" 
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    short_name = f"s{random_suffix}_by_{bot_username}" 
    title = f"تقویم اختصاصی {pack_name}"

    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"

    try:
        for i, img_path in enumerate(images):
            with Image.open(img_path) as img:
                img = img.convert("RGBA")
                img = img.resize((512, 512), Image.Resampling.LANCZOS)
                temp_path = f"ready_{i}.png"
                img.save(temp_path, "PNG")

            with open(temp_path, 'rb') as sticker_file:
                if i == 0:
                    sticker_obj = {'sticker': 'attach://sticker_0', 'emoji_list': ['🗓']}
                    data = {
                        'user_id': user_id,
                        'name': short_name,
                        'title': title,
                        'stickers': json.dumps([sticker_obj]),
                        'sticker_format': 'static'
                    }
                    files = {'sticker_0': sticker_file}
                    resp = requests.post(base_url + "createNewStickerSet", data=data, files=files).json()
                else:
                    sticker_obj = {'sticker': 'attach://sticker_next', 'emoji_list': ['🗓']}
                    data = {
                        'user_id': user_id,
                        'name': short_name,
                        'sticker': json.dumps(sticker_obj)
                    }
                    files = {'sticker_next': sticker_file}
                    resp = requests.post(base_url + "addStickerToSet", data=data, files=files).json()
            
            if os.path.exists(temp_path):
                os.remove(temp_path)

            if not resp.get("ok"):
                print(f"❌ خطا در استیکر {i}: {resp.get('description')}")
                if i == 0: return None 
            else:
                print(f"✅ استیکر {i} با موفقیت اضافه شد.")
                
        return short_name

    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return None