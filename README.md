# 📅 Telegram Calendar Sticker Bot

A professional, high-performance Telegram bot built with **Telethon** and **Pillow (PIL)**. This bot automates the creation of personalized calendar stickers for the Persian (Jalali) months, allowing users to brand their own stickers.

## ✨ Features

- **Automated Sticker Generation**: Creates a full set of 30/31 high-quality stickers for the current month in seconds.
- **Multiple Design Packs**:
  - **Pack 1 (Modern Circle)**: Minimalist circular design for a sleek, modern look.
  - **Pack 2 (Wall Calendar)**: Classic rectangular layout with dual-language support (Persian & English).
- **Advanced State Machine**: Handles user flow smoothly (Brand Name -> ID Collection -> Receipt Upload).
- **Admin Dashboard**: Verification system for payment receipts. Admins can approve or reject orders with inline buttons.
- **RTL Support**: Flawless Persian/Arabic text rendering using `arabic-reshaper` and `python-bidi`.

## 🛠 Tech Stack

- **Core**: Python 3.12+
- **API**: [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto)
- **Image Processing**: [Pillow](https://python-pillow.org/)
- **Date Management**: [jdatetime](https://github.com/slashmili/python-jdatetime)
- **Text Rendering**: `arabic-reshaper` & `python-bidi`

## 🚀 Installation

1. **Clone the Project**:
   ```bash
   git clone [https://github.com/yourusername/sticker-calendar-bot.git](https://github.com/yourusername/sticker-calendar-bot.git)
   cd sticker-calendar-bot
Install Requirements:

Bash

pip install -r requirements.txt
Configuration: Create a config.py file:

Python

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
ADMIN_ID = 12345678 # Your Telegram User ID
Run the Bot:

Bash

python main.py
📂 Project Structure
main.py: Entry point of the application.

handlers/: Contains bot conversation logic and receipt handling.

sticker_factory.py: The engine for rendering and positioning text on images.

database/: Repository logic for user states and orders.

assets/: Templates and fonts.

⚠️ Security Note
Ensure that your *.session files and config.py are NEVER uploaded to public repositories. These files contain sensitive credentials.

📜 License
Distributed under the MIT License. See LICENSE for more information.