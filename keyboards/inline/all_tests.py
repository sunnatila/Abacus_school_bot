from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

all_test_callback_data = CallbackData('test', 'item_id')


def make_all_tests_inlines(is_active, is_premium):
    buttons = InlineKeyboardMarkup(row_width=1)
    if is_active:
        if is_premium:
            tests = db.select_premium_active_sorted_tests()
        else:
            tests = db.select_free_active_sorted_tests()
    else:
        if is_premium:
            tests = db.select_premium_no_active_sorted_tests()
        else:
            tests = db.select_free_no_active_sorted_tests()
    for test in tests:
        class_number = db.select_class(test[8])[1]
        science_name = db.select_science(test[9])[1]
        btn = InlineKeyboardButton(text=f"{class_number}-sinf, {science_name} fani testi: {test[10][:19]}", callback_data=all_test_callback_data.new(item_id=test[0]))
        buttons.insert(btn)
    buttons.insert(InlineKeyboardButton(text='❌', callback_data=all_test_callback_data.new(item_id="back")))
    return buttons


edit_test_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Tahrirlash", callback_data='edit'),
            InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_actives'),
        ],
        [
            InlineKeyboardButton(text='❌', callback_data="back_to_admin_panel")
        ]
    ],
    row_width=2
)


activate_test_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Aktivlashtirish", callback_data='activate'),
            InlineKeyboardButton(text='📊 Statistika', callback_data="statistics"),
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_no_actives'),
            InlineKeyboardButton(text='❌', callback_data="back_to_admin_panel")
        ]
    ],
    row_width=2
)

de_activate_test_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Aktivsizlantirish", callback_data='deactivate'),
            InlineKeyboardButton(text='📊 Statistika', callback_data="statistics"),
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data='back_to_actives'),
            InlineKeyboardButton(text='❌', callback_data="back_to_admin_panel")
        ]
    ],
    row_width=2
)
