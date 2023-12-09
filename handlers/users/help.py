from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Command

from keyboards.default import menu
from loader import dp, db


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("🆗 Quyidagi bo'limlardan birini tanlang ❕\n\n",
            "❇️ Yoki test yechish bo'limidan bepul va pullik testlarimizni yechib o'z sertifikatlaringizni qo'lga kiriting!")
    
    await message.answer("\n".join(text), reply_markup=menu)


@dp.message_handler(Command('menu'), state='*')
async def menu_page(message: types.Message, state):
    await message.delete()
    user = db.select_user(message.from_user.id)
    if user:
        await message.answer("Bo'limni tanlang:", reply_markup=menu)
        await state.finish()
    else:
        await message.answer("Iltimos avval ro'yxatdan o'ting!")
