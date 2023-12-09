from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.deep_linking import get_start_link

from data.config import bot_image
from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), text="👥 Do'stlarni taklif qilish")
async def ref_input(message: types.Message):
    deep_link = await get_start_link(str(message.from_user.id), encode=True)
    ref = f"*Abacus school bot* orqali bir necha fanlardan testlar ishlashingiz va sertifikatlar olishingiz mumkin\.\n" \
          f"Ushbu botni men sizga taklif qilaman 😊\n\n" \
          f"[Abacus school botiga link]({str(deep_link)})\n\n" \
          f"Do'stlarga ulashamiz\!"
    # ref_link = create_ref_link(ref)
    await message.answer_photo(photo=bot_image, caption=ref, parse_mode=ParseMode.MARKDOWN_V2)
