from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("☎️ Kontaktni yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)