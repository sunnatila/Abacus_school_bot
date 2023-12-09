from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("♻️ Ismni tahrirlash"),
            KeyboardButton("♻️ Raqamni tahrirlash")
        ],
        [
            KeyboardButton("ℹ️ Ma'lumotlarim"),
            KeyboardButton("◀️ Orqaga")
        ]
    ],
    resize_keyboard=True
)
