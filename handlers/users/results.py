from typing import Union

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import BadRequest

from filters import IsPrivate
from keyboards.default import result_buttons
from keyboards.inline import result_tests_callback_data, result_tests_inlines, result_test_inline, back_result_inline
from loader import dp, db, bot


@dp.message_handler(IsPrivate(), text="👤 Mening natijam")
async def result_func(message: types.Message):
    text = "👤 Mening natijam"
    await message.answer(text, reply_markup=result_buttons)


@dp.message_handler(IsPrivate(), text="🆓 Bepul test natijasi")
async def show_free_tests(msg: types.Message):
    await list_solved_tests(msg, False)


@dp.message_handler(IsPrivate(), text="💰 Pullik test natijasi")
async def show_premium_tests(msg: types.Message):
    await list_solved_tests(msg, True)


async def list_solved_tests(message: Union[Message, CallbackQuery], premium, **kwargs):
    if isinstance(message, Message):
        await message.answer("Natijani ko'rish uchun testni tanlang:",
                             reply_markup=await result_tests_inlines(message.from_user.id, premium))
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text("Natijani ko'rish uchun testni tanlang:",
                                     reply_markup=await result_tests_inlines(message.from_user.id, premium))


async def show_solved_test(call: CallbackQuery, premium, item_id, **kwargs):
    data = db.select_solvedtest(item_id)
    info = f"⏱ Test boshlangan vaqt: {data[3][:19]}\n\n" \
           f"🏁 Test yakunlangan vaqt: {data[10][:19]}\n\n" \
           f"🔄 Urinishlar soni: {data[4]}\n\n" \
           f"📋 Birinchi urinishdagi ball: {data[5]}\n\n"
    if data[6] is None:
        info += "❌ Sertifikat olinmagan"
    else:
        info += "✅ Sertifikat olingan, yuklab olish uchun 🖨 Sertifikat tugmani bosing"
    await call.message.delete()
    await call.message.answer(info, reply_markup=await result_test_inline(premium, item_id))


async def show_certificate(call: CallbackQuery, premium, item_id, **kwargs):
    data = db.select_solvedtest(item_id)
    await call.message.delete()
    if data[6]:
        try:
            await bot.send_document(call.from_user.id, data[6], caption='Sizning sertifikatingiz!',
                                    reply_markup=await back_result_inline(premium, item_id))
        except BadRequest:
            await call.message.answer("Sertifikatingizda qandaydir xatolik bor!",
                                      reply_markup=await back_result_inline(premium, item_id))
    else:
        await call.message.answer("Sizning bu testdan sertifikatingiz mavjud emas!",
                                  reply_markup=await back_result_inline(premium, item_id))


async def remove_list(call: CallbackQuery, **kwargs):
    await call.message.edit_text("👤 Mening natijam")


@dp.callback_query_handler(result_tests_callback_data.filter())
async def callback_query_func(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    premium = callback_data.get('premium')
    item_id = callback_data.get('item_id')
    levels = {
        '-1': remove_list,
        '0': list_solved_tests,
        '1': show_solved_test,
        '2': show_certificate
    }
    premium = True if premium == 'True' else False
    await levels[level](call, premium=premium, item_id=item_id)


@dp.message_handler(IsPrivate(), text="🧮 Umumiy statistika")
async def result_func(message: types.Message):
    text = f"👤 Botning foydalanuvchilari soni : {db.select_count_users()} ta\n\n" \
           f"📂 Botda faol testlar soni : {db.select_count_active_tests()} ta\n\n" \
           f"📝 Foydalanuvchilar ishlagan testlar soni : {db.select_count_solvedtests()} ta\n\n" \
           f"Ijtimoiy tarmoqlarda <b>Abacus school</b>\n\n" \
           f"🔗 Instagram sahifamiz: <a href='https://www.instagram.com/abacusschool_lc/'>abacusschool_lc</a>\n\n" \
           f"🔗 You tube sahifamiz: <a href='https://www.youtube.com/@abacusschool_lc/'>abacus school_lc</a>"
    await message.answer(text)
