from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

confirm_responses_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="true_responses"),
            InlineKeyboardButton(text="🔄 Qayta kiritish", callback_data="false_responses"),
        ]
    ]
)

premium_or_free_test_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 Pullik", callback_data="premium_test"),
            InlineKeyboardButton(text="🆓 Bepul", callback_data="free_test")
        ],
    ]
)

activate_callback_data = CallbackData('activate', 'state_type')

access_test_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔓 Faollashtirish", callback_data=activate_callback_data.new(state_type='active')),
            InlineKeyboardButton(text="🔒 Faolsizlantirish", callback_data=activate_callback_data.new(state_type='de_active'))
        ],
    ]
)
