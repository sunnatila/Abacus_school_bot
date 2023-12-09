from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import admin_panel_buttons, free_premium_buttons
from keyboards.inline import make_sciences_inlines, make_all_tests_inlines, all_test_callback_data, edit_test_buttons
from loader import dp, db
from states import ChangeTestStateGroup, NewTestStateGroup


@dp.message_handler(IsPrivate(), text="🔄 Testni tahrirlash", user_id=ADMINS)
async def add_new_test(message: types.Message):
    text = "Faqat faol testni tahrirlashingiz mumkin.\n" \
           "Test turini tanlang:"
    await message.answer(text, reply_markup=free_premium_buttons)
    await ChangeTestStateGroup.free_premium.set()


@dp.message_handler(text="⬅️ Orqaga", state=ChangeTestStateGroup.free_premium)
async def back_to_admin_panel(msg: types.Message, state: FSMContext):
    await msg.answer("Admin panel", reply_markup=admin_panel_buttons)
    await state.finish()


@dp.message_handler(text=("🆓 Bepul testlar", "💰 Pullik testlar"), state=ChangeTestStateGroup.free_premium)
async def free_tests_changes(message: types.Message, state: FSMContext):
    if message.text == "💰 Pullik testlar":
        await state.update_data({'premium': True})
    else:
        await state.update_data({'premium': False})
    async with state.proxy() as data:
        is_active = True
        is_premium = data.get('premium')
    await message.answer("Testni tanlang:", reply_markup=make_all_tests_inlines(is_active, is_premium))
    await ChangeTestStateGroup.next()


@dp.callback_query_handler(all_test_callback_data.filter(), state=ChangeTestStateGroup.tests)
async def click_test(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    item_id = callback_data.get('item_id')
    if item_id == "back":
        await call.message.answer("Tanlang:", reply_markup=free_premium_buttons)
        await ChangeTestStateGroup.free_premium.set()
        return
    await state.update_data({"test_id": item_id})
    data = db.select_test(item_id)
    info = f"ℹ️ Test haqida ma'lumot.\n\n" \
           f"🔢 Test sinfi: {db.select_class(data[8])[1]}-sinf\n\n" \
           f"📗 Test fani: {db.select_science(data[9])[1]} fani\n\n" \
           f"📊 Test holati: aktiv ♻️\n\n" \
           f"🔢 Test soni: {data[3]}\n\n" \
           f"📝 Javoblar: {data[4]}\n\n"
    if data[5]:
        info += f"💵 Test pullik va narxi: {data[6]} so'm\n\n"
    info += f"⏳ Test davomiyligi: {data[7]} daqiqa\n\n" \
            f"🕰 Bazaga kiritilgan vaqti: {data[10][:20]}"
    try:
        await call.message.answer_photo(data[2], caption=f"{info}", reply_markup=edit_test_buttons)
    except BadRequest:
        await call.message.answer_document(data[2], caption=f"{info}", reply_markup=edit_test_buttons)
    await ChangeTestStateGroup.next()


@dp.callback_query_handler(text="edit", state=ChangeTestStateGroup.test)
async def activate_test(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Testning ma'lumotlarini qaytadan kiriting.\n"
                              "Testning fanini tanlang:", reply_markup=make_sciences_inlines())
    await NewTestStateGroup.science.set()


@dp.callback_query_handler(text="back_to_actives", state=ChangeTestStateGroup.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        is_active = True
        is_premium = data.get('premium')
    await call.message.answer("Testni tanlang:", reply_markup=make_all_tests_inlines(is_active, is_premium))
    await ChangeTestStateGroup.tests.set()


@dp.callback_query_handler(text="back_to_admin_panel", state=ChangeTestStateGroup.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.reset_data()
    await call.message.answer("Admin panel", reply_markup=admin_panel_buttons)
    await state.finish()


@dp.message_handler(state=ChangeTestStateGroup, content_types=ContentType.ANY)
async def err_send_answer(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos buyruq tugmalaridan foydalaning!")
