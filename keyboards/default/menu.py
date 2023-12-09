from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🧑‍💻️ Test ishlash")
        ],
        [
            KeyboardButton("🛠 Sozlamalar"),
            KeyboardButton("👥 Do'stlarni taklif qilish")
        ],
        [
            KeyboardButton("👤 Mening natijam"),
            KeyboardButton("🧮 Umumiy statistika")
        ]
    ],
    resize_keyboard=True
)
