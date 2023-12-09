from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from keyboards.default import settings, menu, back_button
from loader import dp, db


@dp.message_handler(IsPrivate(), text="🛠 Sozlamalar")
async def settings_func(message: types.Message):
    text = "🛠 Sozlamalar"
    await message.answer(text, reply_markup=settings)


@dp.message_handler(IsPrivate(), text="♻️ Ismni tahrirlash")
async def edit_fullname(message: types.Message, state: FSMContext):
    text = "Yangi ism-familiyani yuboring:"
    await message.answer(text, reply_markup=back_button)
    await state.set_state("new_fullname")


@dp.message_handler(state=("new_fullname", "new_phone"), text="◀️ Orqaga")
async def back_settings(message: types.Message, state: FSMContext):
    text = "🛠 Sozlamalar"
    await message.answer(text, reply_markup=settings)
    await state.finish()


@dp.message_handler(state="new_fullname")
async def update_fullname(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    fullname = message.text
    db.update_user_fullname(user_id, fullname)
    text = "Ismingiz muvaffaqiyatli o'zgartirildi ✅"
    await message.answer(text, reply_markup=settings)
    await state.finish()


@dp.message_handler(IsPrivate(), text="♻️ Raqamni tahrirlash")
async def edit_phone(message: types.Message, state: FSMContext):
    text = "Yangi telefon raqamingizni yuboring:"
    await message.answer(text, reply_markup=back_button)
    await state.set_state("new_phone")


@dp.message_handler(state="new_phone")
async def update_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text
    db.update_user_phone(user_id, phone)
    text = "Telefon raqamingiz muvaffaqiyatli o'zgartirildi ✅"
    await message.answer(text, reply_markup=settings)
    await state.finish()


@dp.message_handler(IsPrivate(), text="ℹ️ Ma'lumotlarim")
async def back_menu(message: types.Message):
    user = db.select_user(message.from_user.id)
    text = f"👤 Ism-familiyangiz: <b>{user[1]}</b>\n" \
           f"☎️ Telefon raqamingiz: {user[2]}\n" \
           f"👥 Do'stlaringiz soni: <b><i>{user[4]}</i></b>"
    await message.answer(text)


@dp.message_handler(IsPrivate(), text="◀️ Orqaga")
async def back_menu(message: types.Message):
    text = "Bo'limni tanlang:"
    await message.answer(text, reply_markup=menu)


