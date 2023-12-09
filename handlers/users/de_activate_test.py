from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import free_premium_buttons, admin_panel_buttons
from keyboards.inline import make_all_tests_inlines, all_test_callback_data, de_activate_test_buttons
from loader import dp, db
from states import DeActiveTestStates


@dp.message_handler(IsPrivate(), text="🔒 Testni faolsizlantirish", user_id=ADMINS)
async def show_tests(msg: types.Message, state: FSMContext):
    await state.update_data({'access': True})
    await msg.answer("Tanlang:", reply_markup=free_premium_buttons)
    await DeActiveTestStates.free_premium.set()


@dp.message_handler(text=("🆓 Bepul testlar", "💰 Pullik testlar"), state=DeActiveTestStates.free_premium)
async def choose_type(msg: types.Message, state: FSMContext):
    if msg.text == "💰 Pullik testlar":
        await state.update_data({'premium': True})
    else:
        await state.update_data({'premium': False})
    async with state.proxy() as data:
        is_active = data.get('access')
        is_premium = data.get('premium')
    await msg.answer("Testni tanlang:", reply_markup=make_all_tests_inlines(is_active, is_premium))
    await DeActiveTestStates.next()


@dp.message_handler(text="⬅️ Orqaga", state=DeActiveTestStates.free_premium)
async def back_to_admin_panel(msg: types.Message, state: FSMContext):
    await msg.answer("Admin panel", reply_markup=admin_panel_buttons)
    await state.finish()


@dp.callback_query_handler(all_test_callback_data.filter(), state=DeActiveTestStates.tests)
async def click_test(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    item_id = callback_data.get('item_id')
    if item_id == "back":
        await call.message.answer("Tanlang:", reply_markup=free_premium_buttons)
        await DeActiveTestStates.free_premium.set()
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
        await call.message.answer_photo(data[2], caption=f"{info}", reply_markup=de_activate_test_buttons)
    except BadRequest:
        await call.message.answer_document(data[2], caption=f"{info}", reply_markup=de_activate_test_buttons)
    await DeActiveTestStates.next()


@dp.callback_query_handler(text="statistics", state=DeActiveTestStates.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    async with state.proxy() as data:
        test_id = data.get('test_id')
        class_num = data.get('class_num')
        science = data.get('science')
    result = db.select_test_solved_tests(test_id)
    result_info = f"{science} fani {class_num}-sinf uchun test natijalari:\n"
    i = 1
    for user_test in result:
        user = db.select_user(user_test[9])
        result_info += f"{i}. {user[1]} - {user_test[5]} ball 👉 {user[3]} - tel: {user[2]}\n"
        print(user)
        i += 1
    await call.message.answer(f"{result_info}", reply_markup=admin_panel_buttons)
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(text="deactivate", state=DeActiveTestStates.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        test_id = data.get('test_id')
    db.update_access_test(test_id)
    await call.message.answer("Admin panel", reply_markup=admin_panel_buttons)
    await call.answer("Test aktivsizlantirildi!", show_alert=True)
    await call.message.delete()
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(text="back_to_actives", state=DeActiveTestStates.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        is_active = data.get('access')
        is_premium = data.get('premium')
    await call.message.answer("Testni tanlang:", reply_markup=make_all_tests_inlines(is_active, is_premium))
    await DeActiveTestStates.tests.set()


@dp.callback_query_handler(text="back_to_admin_panel", state=DeActiveTestStates.test)
async def activate_test(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.reset_data()
    await call.message.answer("Admin panel", reply_markup=admin_panel_buttons)
    await state.finish()


@dp.message_handler(state=DeActiveTestStates, content_types=ContentType.ANY)
async def err_send_answer(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos buyruqlar tugmalaridan foydalaning!")
