from aiogram import types
from aiogram.types import ContentType

from data.config import ADMINS
from keyboards.default import menu, admin_panel_buttons
from loader import dp, bot
from utils.create_certificate import create_certificate


@dp.message_handler(state=None, content_types=ContentType.ANY, user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.delete()
    await message.answer("Biror bo'limni tanlamoqchimisiz?", reply_markup=admin_panel_buttons)


@dp.message_handler(state=None, content_types=ContentType.ANY)
async def bot_echo(message: types.Message):
    await message.delete()
    await message.answer("<b>Iltimos quyidagi tugmalardan foydalaning yoki buyruqlar ketma-ketligiga amal qiling!</b>",
                         reply_markup=menu)
