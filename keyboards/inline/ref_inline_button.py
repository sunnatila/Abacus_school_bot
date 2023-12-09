from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_ref_link(text):
    ref_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📤 Ulashish", switch_inline_query=text)]
        ]
    )
    return ref_button
