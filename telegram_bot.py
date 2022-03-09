from aiogram import types
from create_bot import dp, bot
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from english import english
from russian import russian, other
from admin import admin
from db import users_db
import links
import database


@dp.message_handler(commands=['start'])
async def choose_language(message: types.message):
    markup = InlineKeyboardMarkup(row_width=2)
    rus = InlineKeyboardButton(text='Русский', callback_data="rus_lang")
    eng = InlineKeyboardButton(text='English', callback_data="eng_lang")
    markup.add(rus, eng)
    if users_db.have_user(message.from_user.id):
        await russian.menu(message.from_user.id)
    else:
        await bot.send_message(message.from_user.id,
                               text=links.welcome_text,
                               reply_markup=markup)

russian.register_step_russian(dp)
english.register_step_russian(dp)
admin.register_step_admin(dp)
other.check_text(dp)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
