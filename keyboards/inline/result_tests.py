from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

result_tests_callback_data = CallbackData('solved_test', 'level', 'premium', 'item_id')


async def make_result_cd(level, premium='0', item_id='0'):
    return result_tests_callback_data.new(level=level, premium=premium, item_id=item_id)


async def result_tests_inlines(user_id, is_premium):
    CURRENT_LEVEL = 0
    buttons = InlineKeyboardMarkup(row_width=1)
    solved_tests = db.select_user_solved_tests(user_id)
    for solved_test in solved_tests:
        test = db.select_test(solved_test[8])
        if test[5] != is_premium:
            continue
        class_number = db.select_class(test[8])[1]
        science_name = db.select_science(test[9])[1]
        btn = InlineKeyboardButton(text=f"{class_number}-sinf, {science_name} fani testi: {solved_test[10][:19]}",
                                   callback_data=await make_result_cd(CURRENT_LEVEL+1, f"{is_premium}", item_id=solved_test[0]))
        buttons.insert(btn)
    buttons.insert(InlineKeyboardButton(text='❌', callback_data=await make_result_cd(CURRENT_LEVEL-1)))
    return buttons


async def result_test_inline(is_premium, item_id):
    CURRENT_LEVEL = 1
    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(
        InlineKeyboardButton(
            text="🖨 Sertifikat",
            callback_data=await make_result_cd(CURRENT_LEVEL+1, f"{is_premium}", item_id=item_id)
        )
    )
    buttons.insert(InlineKeyboardButton(text='🔙 Orqaga',
                                        callback_data=await make_result_cd(CURRENT_LEVEL-1, f"{is_premium}")))
    return buttons


async def back_result_inline(is_premium, item_id):
    CURRENT_LEVEL = 2
    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(text='🔙 Orqaga',
                                        callback_data=await make_result_cd(CURRENT_LEVEL - 1, premium=f"{is_premium}", item_id=item_id)))
    return buttons
