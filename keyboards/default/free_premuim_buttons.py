from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

free_premium_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🆓 Bepul testlar"),
            KeyboardButton("💰 Pullik testlar")
        ],
        [
            KeyboardButton("⬅️ Orqaga")
        ]
    ],
    resize_keyboard=True
)


test_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🆓 Bepul test yechish"),
            KeyboardButton("💰 Pullik test yechish")
        ],
        [
            KeyboardButton("◀️ Orqaga")
        ]
    ],
    resize_keyboard=True
)
