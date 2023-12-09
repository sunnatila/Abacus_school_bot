import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS
from keyboards.inline.checksubs import check_button
from utils.misc import subscription
from loader import bot, db


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            if update.message.text == "🧑‍💻️ Test ishlash":
                user = update.message.from_user.id
            else:
                return
        else:
            return

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        for channel in CHANNELS:
            status = await subscription.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                result += f"👉 <a href='{invite_link}'>{channel.title}</a>\n"

        if not final_status:
            await update.message.answer(result, reply_markup=check_button, disable_web_page_preview=True)
            raise CancelHandler()

        user = db.select_user(update.message.from_user.id)
        if user:
            if user[4] >= 0:
                return
            else:
                await update.message.answer(f"‼️ Siz {user[4]}ta do'stingizni taklif qilgansiz!\n\n"
                                            f"👥 Test yechish uchun yana {3-user[4]}ta do'stingizni taklif qiling!")
                raise CancelHandler()
        else:
            await update.message.answer(f"‼️ Siz ro'yxatdan o'tmagansiz!\n\n"
                                        f"🔄 Iltimos ro'yxatdan o'ting! -> /start")
            raise CancelHandler()
