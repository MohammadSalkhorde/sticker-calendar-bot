# 📅 Telegram Calendar Sticker Bot

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Telethon-orange.svg)](https://github.com/LonamiWebs/Telethon)
[![Database](https://img.shields.io/badge/database-MongoDB-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-success.svg)](LICENSE)

A **fully-automated Telegram bot** for generating **professional Persian (Jalali) calendar sticker packs**.  
Designed for businesses and creators who want **custom-branded Telegram stickers** with payment verification and admin control.

---

## ✨ Overview

This bot allows users to:
1. Choose a sticker design pack  
2. Upload a payment receipt  
3. Get admin approval  
4. Automatically receive a **full Telegram sticker pack (1–30/31 days)**  

All stickers are **generated dynamically**, rendered with perfect Persian typography, and uploaded as **real Telegram sticker packs** using MTProto.

---

## 🌟 Key Features

### 🚀 Automation
- Generates **complete monthly sticker packs** in one click
- No manual upload or editing required

### 🎨 Sticker Packs
- **Pack 1 – Modern Circle**  
  Minimal, clean circular design for modern branding
- **Pack 2 – Wall Calendar**  
  Classic calendar-style layout with date focus

### 🧠 Smart User State Machine
User flow is strictly controlled:

### 🛡️ Admin Panel
- Admin receives payment receipts
- Approve ❌ / Confirm ✅ via inline buttons
- Sticker pack is created only after approval

### ✍️ Perfect Persian Typography
- RTL text rendering
- Proper Persian digit shaping
- Powered by:
  - `arabic-reshaper`
  - `python-bidi`

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| Language | Python 3.12+ |
| Telegram API | Telethon (Bot API + MTProto) |
| Image Processing | Pillow (PIL) |
| Calendar | jdatetime (Jalali) |
| Typography | arabic-reshaper, python-bidi |
| Database | MongoDB |

---

## 📂 Project Structure

```text
project/
│
├── assets/                  # PNG templates & fonts
│   ├── pack1/
│   └── pack2/
│
├── database/
│   ├── mongo.py              # MongoDB connection
│   ├── user_repo.py          # User state management
│   └── order_repo.py         # Orders & receipts
│
├── handlers/
│   ├── start.py              # /start command
│   ├── product.py            # Pack selection
│   ├── receipt.py            # Receipt upload & confirmation
│   └── admin.py              # Admin approval & sticker creation
│
├── services/
│   ├── sticker_factory.py    # Calendar image generation
│   ├── image_renderer.py     # Text rendering on images
│   └── telegram_sticker_pack.py # MTProto sticker pack creator
│
├── bot.py                    # Application entry point
├── config.py                 # Credentials & settings (PRIVATE)
├── enums.py                  # User state enums
├── requirements.txt          # Dependencies
└── README.md
