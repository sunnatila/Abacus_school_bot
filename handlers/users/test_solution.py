import os
from datetime import datetime, timedelta
from typing import Union

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message
from aiogram.utils.exceptions import BadRequest

from data.config import click_qr, uzum_qr, xazna_qr, ADMINS, karta, karta_name
from filters import IsPrivate
from keyboards.default import test_type, menu
from keyboards.inline import sciences_keyboards, classes_keyboards, tests_keyboards, solution_test_cd, \
    confirm_button, check_test_button, check_test_cd, confirm_responses_button, buy_button
from keyboards.inline.test_solution import buy2_button, transfer_type_keyboards, transfer_success_keyboards, \
    update_permission_button, admin_check_test_cd, download_certificate_cd, certificate_download
from loader import dp, db, bot
from utils.create_certificate import create_certificate


@dp.message_handler(IsPrivate(), text="🧑‍💻️ Test ishlash")
async def add_new_test(message: types.Message, state: FSMContext):
    await message.answer("Qaysi turdagi test yechmoqchisiz?", reply_markup=test_type)
    await state.set_state('solution_test')


@dp.message_handler(text=("🆓 Bepul test yechish", "💰 Pullik test yechish"), state="solution_test")
async def choose_test_type(message: Message, state: FSMContext):
    if message.text == "💰 Pullik test yechish":
        await state.update_data({'premium': True})
    else:
        await state.update_data({'premium': False})
    await list_sciences(message, state)


@dp.message_handler(text="◀️ Orqaga", state="solution_test")
async def cancel_main(message: Message, state: FSMContext):
    await message.answer("Bo'limni tanlang:", reply_markup=menu)
    await state.finish()


async def list_sciences(message: Union[Message, CallbackQuery], state: FSMContext, **kwargs):
    if isinstance(message, Message):
        await message.answer("Qaysi fandan test yechmoqchisiz? \nTanlang:", reply_markup=await sciences_keyboards())
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text("Qaysi fandan test yechmoqchisiz? \nTanlang:",
                                     reply_markup=await sciences_keyboards())


async def list_classes(call: CallbackQuery, state: FSMContext, science_id, **kwargs):
    await call.message.edit_text("Sinfingizni tanlang:", reply_markup=await classes_keyboards(science_id))


async def list_tests(call: CallbackQuery, state: FSMContext, premium, science_id, class_id, **kwargs):
    if premium:
        info = "✍🏻 Testni yechish uchun testni tanlang!\n\n‼️ Eslatma.\n\n" \
               "Sertifikat faqat 1-urinishda 85 balldan yuqori ball olgan foydalanuvchi uchun beriladi"
    else:
        info = "✍🏻 Testni yechish uchun testni tanlang!\n\n‼️ Eslatma.\n\n" \
               "Sertifikat faqat pullik testlarni yechgan foydalanuvchilar uchun beriladi"
    await call.message.edit_text(info,
                                 reply_markup=await tests_keyboards(call.from_user.id, premium, science_id, class_id))


async def check_confirm(call: CallbackQuery, state: FSMContext, premium, science_id, class_id, item_id, **kwargs):
    solved_test = db.select_user_solvedtest(call.from_user.id, item_id)
    await state.update_data({
        'class_id': class_id,
        'science_id': science_id,
        'test_id': item_id,
    })
    if premium:
        test_price = db.select_test(item_id)[6]
        if solved_test:
            await state.update_data({"urinish": solved_test[4],
                                     'permission': solved_test[1],
                                     'price': test_price})
            if solved_test[1]:
                await call.message.edit_text("Testni boshlash uchun <b>✍🏻 Testni boshlash</b> tugmasini bosing ❕",
                                             reply_markup=await confirm_button(science_id, class_id, item_id))
                return
            else:
                await call.message.edit_text("To'lovingiz adminga yuborilgan, tasdiqlash kutilmoqda!\n\n"
                                             "Agar to'lovda xatolik ketgan bo'lsa, <b>💳 Qayta to'lov</b> tugmasini bosing",
                                             reply_markup=await buy2_button(science_id, class_id, item_id))
        else:
            await state.update_data({"urinish": 0,
                                     'permission': False,
                                     'price': test_price})
            await call.message.edit_text(f"‼️ Testni yechish uchun to'lovni amalga oshiring\n\n"
                                         f"Test narxi: {test_price} so'm\n\n"
                                         f"To'lovni amalga oshirish uchun <b>💳 Karta orqali</b> o'tkazish tugmasini bosing ❕",
                                         reply_markup=await buy_button(science_id, class_id, item_id))
    else:
        if solved_test is None:
            db.add_solvedtest(call.from_user.id, item_id)
            await state.update_data({"urinish": 0,
                                     'permission': True})
        else:
            await state.update_data({"urinish": solved_test[4],
                                     'permission': solved_test[1]})
        await call.message.edit_text("Testni boshlash uchun <b>✍🏻 Testni boshlash</b> tugmasini bosing ❕",
                                     reply_markup=await confirm_button(science_id, class_id, item_id))


async def buy_test(call: CallbackQuery, state: FSMContext, science_id, class_id, item_id, price, **kwargs):
    await call.message.delete()
    await call.message.answer("O'tkazma turini tanlang:",
                              reply_markup=await transfer_type_keyboards(science_id, class_id, item_id, price))
    await state.set_state('solution_test')


async def transfer_await(call: CallbackQuery, state: FSMContext, science_id, class_id, item_id, price, transfer_type,
                         **kwargs):
    await call.message.delete()
    async with state.proxy() as data:
        transfer = data.get('transfer')
    if transfer == 'xazna':
        doc_id = xazna_qr
    elif transfer == 'uzum':
        doc_id = uzum_qr
    else:
        doc_id = click_qr
    if transfer_type == 'karta':
        await call.message.answer(f"💳 Karta raqami: <tg-spoiler>{karta}</tg-spoiler>\n"
                                  f"👤 Karta egasi: <b>{karta_name}</b>\n\n"
                                  f"O'tkazmani amalga oshiring va o'tkazma chekini yuboring 📮",
                                  reply_markup=await transfer_success_keyboards(science_id, class_id, item_id,
                                                                                price, transfer_type))
    else:
        await call.message.answer_document(doc_id,
                                           caption="QR Code ni skaner qiling yoki quyidagi <b>📲 Ilovaga o'tish</b> tugmasini bosing!\n\n"
                                                   "Keyin o'tkazmani amalga oshiring va o'tkazma chekini yuboring 📮",
                                           reply_markup=await transfer_success_keyboards(science_id, class_id, item_id,
                                                                                         price, transfer_type))
    await state.set_state('buy_success')


async def show_test(call: CallbackQuery, state: FSMContext, item_id, **kwargs):
    async with state.proxy() as data:
        urinish = data.get('urinish')
    await call.message.delete()
    test_data = db.select_test(int(item_id))
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    start = datetime.now(tashkent_timezone)
    stop = datetime.now(tashkent_timezone) + timedelta(minutes=test_data[7])
    if urinish == 0:
        db.start_progress_solvedtest(call.from_user.id, item_id, start, stop)
    else:
        db.update_quantity_solvedtest(call.from_user.id, item_id)
    await state.update_data({
        'test_id': test_data[0],
        'quantity': test_data[3],
        'test_responses': test_data[4],
        'stop': stop})
    test_info = f"<b>🔢 Test savollar soni: </b>{test_data[3]}\n\n" \
                f"<b>⏳ Test yechish uchun berilgan vaqt: </b>{test_data[7]} daqiqa\n\n" \
                f"<b>⏱ Boshlangan vaqt: </b>\n{start.strftime('%H:%M:%S, %d-%m')}\n\n" \
                f"<b>⏲ Tugash vaqti: </b>\n{stop.strftime('%H:%M:%S, %d-%m')}\n\n" \
                f"<i><b>❗️ Test javoblarini shu vaqt oralig'ida yubormasangiz, testdan olgan ballingiz 0 ball deb baholanadi</b></i>"
    try:
        await call.message.answer_photo(test_data[2], caption=test_info, reply_markup=await check_test_button(item_id))
    except BadRequest:
        await call.message.answer_document(test_data[2], caption=test_info,
                                           reply_markup=await check_test_button(item_id))
    await state.set_state('check_test_result')


async def remove_item(call: CallbackQuery, state: FSMContext, **kwargs):
    await call.message.delete()
    await call.message.answer("Bo'limni tanlang:", reply_markup=menu)
    await state.finish()


@dp.callback_query_handler(solution_test_cd.filter(), state=('solution_test', 'buy_success'))
async def callback_handler(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        premium = data.get('premium')
        permission = data.get('permission')
        price = data.get('price')
    level = callback_data.get('level')
    science_id = callback_data.get('science_id')
    class_id = callback_data.get('class_id')
    test_id = callback_data.get('test_id')
    transfer = callback_data.get('transfer')
    await state.update_data({'transfer': transfer})

    levels = {
        '-1': remove_item,
        '0': list_sciences,
        '1': list_classes,
        '2': list_tests,
        '3': check_confirm,
        '4': show_test if permission else buy_test,
        '5': transfer_await,
    }

    current_func = levels[level]
    await current_func(call, state, premium=premium, science_id=science_id, class_id=class_id, item_id=test_id,
                       price=price, transfer_type=transfer)


@dp.message_handler(state="buy_success", content_types=(ContentType.PHOTO, ContentType.DOCUMENT))
async def send_admin_buy_test(msg: Message, state: FSMContext):
    try:
        file_id = msg.photo[-1].file_id
    except IndexError:
        file_id = msg.document.file_id
    async with state.proxy() as data:
        class_id = data.get('class_id')
        science_id = data.get('science_id')
        price = data.get('price')
        test_id = data.get('test_id')
        transfer = data.get('transfer')
    await state.update_data({'file_id': file_id})
    user_id = msg.from_user.id
    if db.select_user_solvedtest(user_id, test_id) is None:
        db.add_solvedtest(user_id, test_id, file_id)
    else:
        db.update_check_image_solved_test(user_id, test_id, file_id)
    science, class_num = db.select_science(science_id)[1], db.select_class(class_id)[1]
    admin_text = f"👤 User_id: {user_id}\n" \
                 f"Fullname: {msg.from_user.get_mention()}\n\n" \
                 f"♻️ {class_num}-sinf {science} fani testi uchun <b>{transfer}</b> orqali pul o'tkazma amalgan oshirdi!\n\n" \
                 f"💵 Test narxi: {price}\n\n" \
                 f"❓ Test yechishga ruxsat berasizmi?"
    try:
        await bot.send_photo(ADMINS[0], photo=file_id, caption=admin_text,
                             reply_markup=await update_permission_button(test_id, user_id, transfer))
    except BadRequest:
        await bot.send_document(ADMINS[0], document=file_id, caption=admin_text,
                                reply_markup=await update_permission_button(test_id, user_id, transfer))
    await msg.answer("📨 Chekingiz adminga yuborildi!\n\n"
                     "🔄 Chekingizni tekshirib, test yechishingizga ruxsat beriladi!\n\n"
                     "⚠️ Iltimos kuting tez fursatda ruxsat beriladi!", reply_markup=menu)
    await state.finish()


@dp.callback_query_handler(admin_check_test_cd.filter(), user_id=ADMINS)
async def update_permission_func(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    user_id = callback_data.get('user_id')
    test_id = callback_data.get('test_id')
    permission = callback_data.get('permission')
    transfer = callback_data.get('transfer')
    test_data = db.select_test(test_id)
    science, class_num = db.select_science(test_data[9])[1], db.select_class(test_data[8])[1]
    admin_text = f"👤 User_id: {user_id}\n" \
                 f"Fullname: {db.select_user(user_id)[3]}\n\n" \
                 f"♻️ {class_num}-sinf {science} fani testi uchun <b>{transfer}</b> orqali pul o'tkazma amalgan oshirdi!\n\n" \
                 f"💵 Test narxi: {test_data[6]}\n\n"
    if permission == 'true':
        db.update_permission_solvedtest(user_id, test_id)
        admin_text += "✅ Ruxsat berildi!"
        await bot.send_message(user_id,
                               text=f"✅ Xarid qilgan {science} fani {class_num}-sinf uchun testni yechishga ruxsat berildi 🥳\n\n"
                                    f"Ruxsat berilgan test ✔️ shunday belgi bilan ko'rsatilgan ❕")
    else:
        admin_text += "🚫 Rad etildi!"
        await bot.send_message(user_id,
                               text=f"Xarid qilgan {science} fani {class_num}-sinf uchun testni yechish uchun ruxsat berilmadi 😔\n\n"
                                    f"Rad etilganlik haqida ma'lumot olish uchun /admin ga murojat qiling!")
    file_id = db.select_user_solvedtest(user_id, test_id)[7]
    try:
        await bot.send_photo(ADMINS[0], photo=file_id, caption=admin_text)
    except BadRequest:
        await bot.send_document(ADMINS[0], document=file_id, caption=admin_text)


@dp.callback_query_handler(check_test_cd.filter(), state='*')
async def check_test(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    test_id = callback_data.get('test_id')
    async with state.proxy() as data:
        stop = data.get('stop')
        count = data.get('quantity')
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent_timezone)
    if now > stop:
        db.stop_progress_solvedtest(call.from_user.id, test_id, 0)
        await call.message.answer("Testga berilgan vaqt tugadi!\n"
                                  "Siz bu testdan 0% ko'rsatgich bilan yakunladingiz!", reply_markup=menu)
        await state.reset_data()
        await state.finish()
    else:
        await call.message.answer(f"Yaxshi, savollar soni {count} ta ✅\n\n"
                                  f"Javoblarni quyidagi ko'rinishda yuboring :\n"
                                  f"abcdabcd... ({count} ta)\n\n"
                                  f"(Katta harflar bo'lishi ham mumkin)\n\n"
                                  f"Javoblar qanday tartibda qabul qilinadi : \n"
                                  f"1 - savolning javobi a\n"
                                  f"2 - savolning javobi b\n"
                                  f"3 - savolning javobi c bo'ladi.\n\n"
                                  f"Yuqorida ko'rsatilganidek javoblarni ketma-ketlikda yuboring ❗️", reply_markup=ReplyKeyboardRemove())
        await state.set_state("result_test")


@dp.message_handler(state='result_test')
async def check_result_test(msg: Message, state: FSMContext):
    await msg.delete()
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
        confirm_text += "\n\nTest javoblari to'g'ri kiritilganini tasdiqlang ‼️"
        await state.update_data({'responses': responses})
        await msg.answer(confirm_text, reply_markup=confirm_responses_button)
        await state.set_state('send_responses')
    else:
        if len(responses) > quantity:
            natija = (len(responses) - quantity, 'ko\'p')
        else:
            natija = (quantity - len(responses), 'kam')
        await msg.answer(f"Siz {natija[0]}ta {natija[1]} javob yubordingiz. Qayta kiriting:")


@dp.callback_query_handler(text="true_responses", state='send_responses')
async def check_responses_test(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        test_id = data.get('test_id')
        res = data.get("responses")
        test = data.get('test_responses')
        quantity = int(data.get('quantity'))
        urinish = data.get('urinish')
        stop = data.get('stop')
        class_id = data.get('class_id')
        science_id = data.get('science_id')
        premium = data.get('premium')
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent_timezone)
    if now > stop:
        if urinish == 0:
            db.stop_progress_solvedtest(call.from_user.id, test_id, 0)
        await call.message.answer("🚫 Testga berilgan vaqt tugadi!\n\n"
                                  "😔 Siz bu testdan 0% ko'rsatgich bilan yakunladingiz!", reply_markup=menu)
        await state.reset_data()
        await state.finish()
        return
    science, class_number = db.select_science(science_id)[1], db.select_class(class_id)[1]
    true_responses = tuple(filter(lambda index: res[index] == test[index], range(quantity)))
    ball = round(len(true_responses) / quantity * 100)
    confirm_text = f"Siz {urinish + 1}-urinishda {science} fani {class_number}-sinf testidan 100 balldan <b>{ball}</b> ball to'pladingiz!:\n"
    blank = 10 * "  "
    for i in range(1, quantity // 2 + 1):
        n = i + quantity // 2
        confirm_text += f"""\n{i} - {"✅" if res[i - 1] == test[i - 1] else "❌"}{blank}{n} - {"✅" if res[n - 1] == test[n - 1] else "❌"}"""
    if quantity % 2 == 1:
        confirm_text += f"""\n        {blank}{quantity} - {"✅" if res[-1] == test[-1] else "❌"}"""
    if ball >= 85:
        if urinish == 0:
            if premium:
                confirm_text += "\n\nSizni sertifikat bilan tabriklaymiz 🥳️"
                fullname = db.select_user(user_id=call.from_user.id)[1]
                message = await call.message.answer(confirm_text)
                photo = create_certificate(call.from_user.id, test_id, fullname, science, class_number,
                                           now.date())
                with open(photo, 'rb') as file:
                    message_id = await bot.send_document('5232052738', document=file, caption='sertifikat')
                    certificate = message_id.document.file_id
                db.stop_progress_solvedtest(call.from_user.id, test_id, ball, certificate=certificate)
                await message.edit_reply_markup(
                                          reply_markup=await certificate_download(call.from_user.id, test_id))
                try:
                    os.remove(photo)
                except OSError as xatolik:
                    print(f"{photo} o'chirishda xatolik yuz berdi: {xatolik}")
            else:
                confirm_text += "\n\nSizni yuqori ball bilan tabriklayman 🥳️"
                db.stop_progress_solvedtest(call.from_user.id, test_id, ball, certificate=None)
                await call.message.answer(confirm_text)
        else:
            confirm_text += "\n\nSizni yuqori ball bilan tabriklayman 🥳️"
            await call.message.answer(confirm_text)
    else:
        if urinish == 0:
            if premium:
                confirm_text += "\n\nSiz sertifikat ololmadingiz ❗️\nBoshqa testlarimizda o'zingizni sinab ko'ring!"
                db.stop_progress_solvedtest(call.from_user.id, test_id, ball, certificate=None)
            else:
                confirm_text += "\n\nBoshqa testlarimizda o'zingizni sinab ko'ring!"
                db.stop_progress_solvedtest(call.from_user.id, test_id, ball, certificate=None)
        else:
            confirm_text += "\n\nBoshqa testlarimizda o'zingizni sinab ko'ring!"
        await call.message.answer(confirm_text)
    await call.message.answer("Bo'limni tanlang:", reply_markup=menu)
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(download_certificate_cd.filter(), state='*')
async def send_certificate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data.get('user_id')
    test_id = callback_data.get('test_id')
    data = db.select_user_solvedtest(user_id, test_id)
    await call.message.delete()
    if data[6]:
        try:
            await bot.send_document(call.from_user.id, data[6], caption='Sizning sertifikatingiz!')
        except BadRequest:
            await call.message.answer("Sertifikatingizda qandaydir xatolik bor!")
    else:
        await call.message.answer("Sizning bu testdan sertifikatingiz mavjud emas!")


@dp.callback_query_handler(text="false_responses", state='send_responses')
async def change_responses(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Javoblarni qayta yuboring :")
    await state.set_state('result_test')


@dp.message_handler(state="buy_success",
                    content_types=ContentType.ANY)
async def err_choose_type(msg: Message):
    await msg.delete()
    await msg.answer("Iltimos to'lov chekingizni yuboring!")


@dp.message_handler(state=("solution_test", "check_test_result", "result_test", "send_responses", "buy_success"),
                    content_types=ContentType.ANY)
async def err_choose_type(msg: Message):
    await msg.delete()
    await msg.answer("Iltimos test ishlash ketma-ketligiga amal qiling!")
