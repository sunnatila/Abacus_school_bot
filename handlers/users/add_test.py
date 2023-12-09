from datetime import datetime

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import admin_panel_buttons
from keyboards.inline import make_sciences_inlines, make_class_inlines, settings_callback_data, \
    confirm_responses_button, \
    premium_or_free_test_button, access_test_button, activate_callback_data
from loader import dp, db
from states import NewTestStateGroup


@dp.message_handler(IsPrivate(), text="🆕 Yangi test qo'shish", user_id=ADMINS)
async def add_new_test(message: types.Message):
    text = "Testning fanini tanlang:"
    await message.answer(text, reply_markup=make_sciences_inlines())
    await NewTestStateGroup.science.set()


@dp.callback_query_handler(settings_callback_data.filter(), state=NewTestStateGroup)
async def science_class_click(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id')
    name = callback_data.get('name')
    if item_id == 'back':
        await call.message.delete()
        await call.message.answer("Admin panel", reply_markup=admin_panel_buttons)
        await state.finish()
        return
    if name == 'science':
        await state.update_data({'science_id': item_id})
        await call.message.edit_text("Testning sinfini tanlang:", reply_markup=make_class_inlines())
    elif name == 'class':
        await state.update_data({'class_id': item_id})
        await call.message.delete()
        await call.message.answer("Test savollar faylini yuboring!")
    await NewTestStateGroup.next()


@dp.message_handler(state=NewTestStateGroup.question, content_types=(ContentType.DOCUMENT, ContentType.PHOTO))
async def send_question(message: types.Message, state: FSMContext):
    try:
        doc_id = message.document.file_id
    except AttributeError:
        doc_id = message.photo[-1].file_id
    await state.update_data({'question': doc_id})
    await message.answer("Testlar sonini kiriting:")
    await NewTestStateGroup.next()


@dp.message_handler(state=NewTestStateGroup.question, content_types=ContentType.ANY)
async def err_send_question(message: types.Message):
    await message.delete()
    await message.answer("Iltimos Test savollari uchun fayl yoki rasm yuboring!")


@dp.message_handler(state=NewTestStateGroup.quantity)
async def send_quantity(msg: types.Message, state: FSMContext):
    await state.update_data({'quantity': msg.text})
    await msg.answer("Test javoblarini kiriting.\n"
                     "Kiritish tartibi: abcdabcd...")
    await NewTestStateGroup.next()


@dp.message_handler(state=NewTestStateGroup.responses)
async def send_responses(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        quantity = int(data.get('quantity'))
    responses = msg.text.lower().strip()
    error = "Xatolik ❗️\n\nJavoblar faqat a,b,c,d harflaridan iborat bo'lsin ❗️\n\n Javoblarni qayta yuboring :"
    xato_javoblar = tuple(filter(lambda harf: harf.lower() not in 'abcd', responses))
    if len(xato_javoblar):
        await msg.answer(error)
        return
    if len(responses) == quantity:
        confirm_text = "Javoblari to'g'ri kiritilganligini tekshiring:\n"
        blank = 10 * "  "
        for i in range(1, quantity // 2 + 1):
            n = i + quantity // 2
            confirm_text += f"""\n{i} - {responses[i - 1]}{blank}{n} - {responses[n - 1]}"""
        if quantity % 2 == 1:
            confirm_text += f"""\n        {blank}{quantity} - {responses[-1]}"""
        confirm_text += "\n\nTest javoblari to'g'ri kiritilganini tasdiqlang‼️"
        await state.update_data({'responses': responses})
        await msg.answer(confirm_text, reply_markup=confirm_responses_button)
    else:
        if len(responses) > quantity:
            natija = (len(responses) - quantity, 'ko\'p')
        else:
            natija = (quantity - len(responses), 'kam')
        await msg.answer(f"Siz {natija[0]}ta {natija[1]} javob yubordingiz. Qayta kiriting:")


@dp.callback_query_handler(text="true_responses", state=NewTestStateGroup.responses)
async def true_responses(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Test vaqtini kiriting (daqiqada):")
    await NewTestStateGroup.next()


@dp.callback_query_handler(text="false_responses", state=NewTestStateGroup.responses)
async def true_responses(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Javoblarni qayta kiriting:")


@dp.message_handler(state=NewTestStateGroup.time)
async def send_test_time(msg: types.message, state: FSMContext):
    await state.update_data({'time': int(msg.text)})
    await msg.answer("Test pullikmi yoki bepul?", reply_markup=premium_or_free_test_button)
    await NewTestStateGroup.next()


@dp.callback_query_handler(text="premium_test", state=NewTestStateGroup.premium)
async def premium_test_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data({"premium": True})
    await call.message.answer("Test narxini kiriting (so'm):")
    await NewTestStateGroup.next()


@dp.callback_query_handler(text="free_test", state=NewTestStateGroup.premium)
async def free_test_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data({"premium": False, 'amount': 0})
    await call.message.answer("Test hozirdan faollashsinmi?", reply_markup=access_test_button)
    await NewTestStateGroup.access.set()


@dp.message_handler(state=NewTestStateGroup.amount)
async def send_test_amount(msg: types.Message, state: FSMContext):
    await state.update_data({'amount': msg.text})
    await msg.answer("Test hozirdan faollashsinmi?", reply_markup=access_test_button)
    await NewTestStateGroup.next()


@dp.callback_query_handler(activate_callback_data.filter(), state=NewTestStateGroup.access)
async def free_test_yes(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("state_type") == 'active':
        access = True
    else:
        access = False
    await call.message.delete()
    await state.update_data({'access': access})
    async with state.proxy() as data:
        all_data = dict(data)
    info = f"ℹ️ Test haqida ma'lumot.\n\n"
    if access:
        info += f"📊 Test holati: aktiv ♻️\n\n" \
                f"🔢 Test sinfi: {db.select_class(all_data.get('class_id'))[1]}-sinf\n\n" \
                f"📗 Test fani: {db.select_science(all_data.get('science_id'))[1]} fani\n\n"
    else:
        info += f"📊 Test holati: aktiv emas 🚫\n\n"
    info += f"🔢 Test soni: {all_data.get('quantity')}\n\n" \
            f"📝 Javoblar: {all_data.get('responses')}\n\n"
    if all_data.get('premium'):
        info += f"💵 Test pullik va narxi: {all_data.get('amount')} so'm\n\n"
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    info += f"⏳ Test davomiyligi: {all_data.get('time')} daqiqa\n\n" \
            f"🕰 Bazaga kiritilish vaqti: {datetime.now(tashkent_timezone).strftime('%m-%d-%Y, %H:%M:%S')}\n\n" \
            f"Testni bazaga saqlash uchun ruxsat bering:"
    try:
        await call.message.answer_photo(all_data.get('question'), caption=f"{info}",
                                        reply_markup=confirm_responses_button)
    except BadRequest:
        await call.message.answer_document(all_data.get('question'), caption=f"{info}", reply_markup=confirm_responses_button)
    await NewTestStateGroup.next()


@dp.callback_query_handler(text="true_responses", state=NewTestStateGroup.confirm)
async def free_test_yes(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        test_id = data.get('test_id')
        science_id = data.get('science_id')
        class_id = data.get('class_id')
        question_file_id = data.get("question")
        quantity = data.get("quantity")
        responses = data.get("responses")
        time = data.get("time")
        premium = data.get("premium")
        amount = data.get("amount")
        access = data.get("access")
    if test_id:
        db.update_test(test_id, class_id, science_id, question_file_id, quantity, responses, time, premium, amount,
                       access)
    else:
        db.add_test(class_id, science_id, question_file_id, quantity, responses, time, premium, amount, access)
    await call.message.delete()
    await call.message.answer(f"Test bazaga saqlandi!", reply_markup=admin_panel_buttons)
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(text="false_responses", state=NewTestStateGroup.confirm)
async def free_test_yes(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Test fanini tanlang:", reply_markup=make_sciences_inlines())
    await NewTestStateGroup.science.set()


@dp.message_handler(state=NewTestStateGroup, content_types=ContentType.ANY)
async def err_send_answer(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos buyruqlar tugmalaridan foydalaning yoki so'ralgan ma'lumotni yuboring!")
