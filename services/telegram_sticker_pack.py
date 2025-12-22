import os
from telethon.tl.functions.stickers import CreateStickerSetRequest, AddStickerToSetRequest
from telethon.tl.types import InputDocument, DocumentAttributeSticker
from PIL import Image

async def create_sticker_pack(client, user_id, pack_name, images):
    """
    ساخت پک استیکر تلگرام با MTProto
    client: TelegramClient (MTProto)
    user_id: اکانت واقعی
    pack_name: نام پک
    images: لیست مسیر عکس‌ها
    """

    short_name = f"{pack_name}_bybot"

    # resize و تبدیل به png با سایز 512x512
    resized_images = []
    for img_path in images:
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((512, 512))
        out_path = img_path.replace(".jpg", ".png").replace(".jpeg", ".png")
        img.save(out_path)
        resized_images.append(out_path)

    # اولین عکس برای ایجاد پک
    first_file = await client.upload_file(resized_images[0])

    # ایجاد پک استیکر
    await client(CreateStickerSetRequest(
        user_id=user_id,
        title=f"پک {pack_name}",
        short_name=short_name,
        stickers=[InputDocument(
            id=first_file.id,
            parts=first_file.parts,
            name=os.path.basename(first_file.name),
            mime_type='image/png',
            attributes=[DocumentAttributeSticker(alt=f"{pack_name} 1", stickerset=short_name)]
        )]
    ))

    # اضافه کردن باقی استیکرها
    for i, img_path in enumerate(resized_images[1:], start=2):
        file = await client.upload_file(img_path)
        await client(AddStickerToSetRequest(
            user_id=user_id,
            short_name=short_name,
            stickers=[InputDocument(
                id=file.id,
                parts=file.parts,
                name=os.path.basename(file.name),
                mime_type='image/png',
                attributes=[DocumentAttributeSticker(alt=f"{pack_name} {i}", stickerset=short_name)]
            )]
        ))

    return short_name
