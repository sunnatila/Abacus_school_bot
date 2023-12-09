from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import admin_panel_buttons, back_button
from keyboards.default.admin_panel import add_remove_science_buttons, add_remove_class_buttons
from keyboards.inline import make_sciences_inlines, make_class_inlines, settings_callback_data
from loader import dp, db


@dp.message_handler(Command('admin'), IsPrivate(), user_id=ADMINS)
async def admin_panel(message: types.Message):
    await message.answer("Admin panel", reply_markup=admin_panel_buttons)


@dp.message_handler(Command('admin'), IsPrivate())
async def admin_panel(message: types.Message):
    await message.answer("👨‍💻 Admin bilan bog'lanish uchun <a href='https://t.me/chatgpt_2023_new_bot'>tugmani bosing</a>")


@dp.message_handler(IsPrivate(), text="⬅️ Orqaga", user_id=ADMINS)
async def back_menu(message: types.Message):
    text = "Admin panel"
    await message.answer(text, reply_markup=admin_panel_buttons)


@dp.message_handler(IsPrivate(), text="📚 Fanlar", user_id=ADMINS)
async def science_add_remove(msg: types.Message):
    await msg.answer("Buyruqni tanlang:", reply_markup=add_remove_science_buttons)


@dp.message_handler(IsPrivate(), text="🆕 Yangi fan qo'shish", user_id=ADMINS)
async def add_science(msg: types.Message, state: FSMContext):
    await msg.answer("Fan nomini kiriting:", reply_markup=back_button)
    await state.set_state('add_science')


@dp.message_handler(state="add_science", text="◀️ Orqaga")
async def back_settings(message: types.Message, state: FSMContext):
    text = "Buyruqni tanlang:"
    await message.answer(text, reply_markup=add_remove_science_buttons)
    await state.finish()


@dp.message_handler(state='add_science')
async def add_science_success(msg: types.Message, state: FSMContext):
    db.add_science(msg.text)
    await msg.answer("Fan muvaffaqiyatli qo'shildi!", reply_markup=add_remove_science_buttons)
    await state.finish()


@dp.message_handler(IsPrivate(), text="🔄 Fanni o'zgartirish", user_id=ADMINS)
async def remove_science_list(msg: types.Message, state: FSMContext):
    await msg.delete()
    await msg.answer("O'zgartirish uchun fanni tanlang:", reply_markup=make_sciences_inlines())
    await state.set_state('change_science')


@dp.callback_query_handler(settings_callback_data.filter(), state=('change_science', 'change_class'))
async def class_science_lists(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id')
    name = callback_data.get('name')
    await state.update_data({'item_id': item_id})
    if item_id == 'back':
        await call.answer("Buyruqni tanlang:")
        await call.message.delete()
        await state.finish()
        return
    await call.message.delete()
    if name == "science":
        await call.message.answer(f"Fanning yangi nomini kiriting:")
        await state.set_state('set_science_name')
    elif name == 'class':
        await call.message.answer(f"Sinfning yangi qiymatini kiriting:")
        await state.set_state('set_class_name')


@dp.message_handler(state="set_science_name")
async def set_science(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        science_id = data.get('item_id')
    db.update_science(science_id, msg.text)
    await msg.answer("Fanning nomi muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(state="set_class_name")
async def set_science(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        class_id = data.get('item_id')
    db.update_class(class_id, msg.text)
    await msg.answer("Sinf muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(IsPrivate(), text="🔢 Sinflar", user_id=ADMINS)
async def science_add_remove(msg: types.Message):
    await msg.answer("Buyruqni tanlang:", reply_markup=add_remove_class_buttons)


@dp.message_handler(IsPrivate(), text="🆕 Yangi sinf qo'shish", user_id=ADMINS)
async def add_science(msg: types.Message, state: FSMContext):
    await msg.answer("Sinfni kiriting:", reply_markup=back_button)
    await state.set_state('add_class')


@dp.message_handler(state="add_class", text="◀️ Orqaga")
async def back_settings(message: types.Message, state: FSMContext):
    text = "Buyruqni tanlang:"
    await message.answer(text, reply_markup=add_remove_class_buttons)
    await state.finish()


@dp.message_handler(state='add_class')
async def add_science_success(msg: types.Message, state: FSMContext):
    db.add_class(msg.text)
    await msg.answer("Sinf muvaffaqiyatli qo'shildi!", reply_markup=add_remove_class_buttons)
    await state.finish()


@dp.message_handler(IsPrivate(), text="🔄 Sinfni o'zgartirish", user_id=ADMINS)
async def remove_class_list(msg: types.Message, state: FSMContext):
    await msg.delete()
    await msg.answer("O'chirish uchun Sinfni tanlang:", reply_markup=make_class_inlines())
    await state.set_state('change_class')


@dp.message_handler(content_types=(ContentType.DOCUMENT, ContentType.PHOTO), state=('change_science', 'change_class'))
async def err_send_message(msg: types.Message):
    try:
        await msg.answer(msg.photo[-1].file_id)
    except (AttributeError, IndexError):
        await msg.answer(msg.document.file_id)


@dp.message_handler(content_types=ContentType.ANY, state=('change_science', 'change_class'))
async def err_send_message(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos yuqoridagi tugmalardan foydalaning!")
