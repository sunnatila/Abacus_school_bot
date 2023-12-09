from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove, ContentType
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import decode_payload

from data.config import CHANNELS
from filters import IsPrivate
from keyboards.default import contact, menu
from keyboards.inline.checksubs import check_button
from loader import bot, dp, db
from utils.misc import subscription


@dp.message_handler(CommandStart(), IsPrivate())
async def show_channels(message: types.Message, state: FSMContext):
    args = message.get_args()
    reference = decode_payload(args)
    user_id = message.from_user.id
    user = db.select_user(user_id)
    if user is None:
        if reference:
            ref_user = db.select_user(reference)[1]
            db.update_suggestion(reference)
            info = f"👋 Assalomu alaykum {message.from_user.full_name} botimizga xush keldingiz!\n" \
                   f"🫂 Sizni {ref_user} taklif qildi!\n\n"
        else:
            info = f"👋 Assalomu alaykum {message.from_user.full_name} botimizga xush keldingiz!\n\n"
    else:
        info = str()
    channels_format = str()
    check_subscription = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=user_id,
                                          channel=channel)
        if not status:
            check_subscription = False
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        # logging.info(invite_link)
        channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
    if check_subscription:
        if user:
            await message.answer("Bo'limni tanlang:", reply_markup=menu)
            return
        info += "👤 Siz haqingizda bilishimiz uchun iltimos ism-familiyangizni kiriting.\n\n" \
                "‼️ Bu ma'lumot olgan sertifikatingizda ko'rinadi!"
        await message.answer(info, reply_markup=ReplyKeyboardRemove())
        await state.set_state('fullname')
        return
    info += f"Quyidagi kanallarga obuna bo'ling:\n{channels_format}"
    await message.answer(info,
                         reply_markup=check_button,
                         disable_web_page_preview=True)
    await state.set_state('check_sub')


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    check_subscription = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"✅ <b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            check_subscription = False
            invite_link = await channel.export_invite_link()
            result += (f"‼️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")
    if check_subscription:
        await call.message.delete()
    await call.message.answer(result, disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs", state='check_sub')
async def checker(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = db.select_user(user_id)
    await call.answer()
    result = str()
    check_subscription = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"✅ <b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            check_subscription = False
            invite_link = await channel.export_invite_link()
            result += (f"‼️ <b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")
    if check_subscription:
        await call.message.delete()
        if user:
            await call.message.answer("✅ Barcha kanallarga obuna bo'ldingiz!\n"
                                      "Bo'limni tanlang", reply_markup=menu)
            await state.finish()
            return
        await call.message.answer("✅ Barcha kanallarga obuna bo'ldingiz!\n\n"
                                  "👤 Siz haqingizda bilishimiz uchun iltimos ism-familiyangizni kiriting.\n\n"
                                  "‼️  Bu ma'lumot olgan sertifikatingizda ko'rinadi!", reply_markup=ReplyKeyboardRemove())
        await state.set_state('fullname')
        return
    await call.message.answer(result, disable_web_page_preview=True)


@dp.message_handler(content_types=ContentType.ANY, state="check_sub")
async def err_check_subc(msg: types.Message):
    await msg.answer("Iltimos kanallarga a'zo bo'lib keyin, Obunani tekshirish tugmasini boring!")


@dp.message_handler(state='fullname')
async def send_fullname(msg: types.Message, state: FSMContext):
    await state.update_data({'fullname': msg.text})
    await msg.answer("Kontaktingizni yuboring!", reply_markup=contact)
    await state.set_state('phone')


@dp.message_handler(state='phone', content_types='contact', is_sender_contact=True)
async def send_contact(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    phone = msg.contact.phone_number
    mention = msg.from_user.get_mention()
    async with state.proxy() as data:
        fullname = data.get('fullname')
    db.add_user(user_id, fullname, phone, mention)
    await msg.answer("✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n"
                     "Bo'limni tanlang:", reply_markup=menu)
    await state.finish()


@dp.message_handler(state='phone', content_types=ContentType.ANY)
async def err_send_contact(msg: types.Message):
    await msg.answer("Iltimos kontaktiingizni yuboring!", reply_markup=contact)
