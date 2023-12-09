from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

result_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🆓 Bepul test natijasi"),
            KeyboardButton("💰 Pullik test natijasi")
        ],
        [
            KeyboardButton("◀️ Orqaga")
        ]
    ],
    resize_keyboard=True
)
