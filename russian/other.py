from aiogram import Dispatcher, types
from create_bot import dp, bot
from russian import constants, russian
from db import users_db
from aiogram import types
import links


async def choose_language(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await russian.menu(message.from_user.id)
    else:
        await bot.send_message(message.from_user.id, text=links.welcome_text, parse_mode='Markdown')
        await russian.change_city(message)


async def message_filter(message: types.Message):
    await bot.send_message(message.from_user.id, constants.wrong_name)


def check_text(dp: Dispatcher):
    dp.register_message_handler(choose_language, commands=['start'])
    dp.register_message_handler(message_filter)
