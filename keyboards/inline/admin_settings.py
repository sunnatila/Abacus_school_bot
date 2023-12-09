from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

settings_callback_data = CallbackData('datas', 'name', 'item_id')


def make_sciences_inlines():
    buttons = InlineKeyboardMarkup(row_width=2)
    sciences = db.select_sciences()
    for sc in sciences:
        btn = InlineKeyboardButton(text=f"{sc[1]}", callback_data=settings_callback_data.new(name='science', item_id=sc[0]))
        buttons.insert(btn)
    buttons.insert(InlineKeyboardButton(text='❌', callback_data=settings_callback_data.new(name='science', item_id="back")))
    return buttons


def make_class_inlines():
    buttons = InlineKeyboardMarkup(row_width=2)
    classes = db.select_classes()
    for sc in classes:
        btn = InlineKeyboardButton(text=f"{sc[1]}-sinf", callback_data=settings_callback_data.new(name='class', item_id=sc[0]))
        buttons.insert(btn)
    buttons.insert(InlineKeyboardButton(text='❌', callback_data=settings_callback_data.new(name='class', item_id="back")))
    return buttons
