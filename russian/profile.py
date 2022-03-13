from aiogram import types
from create_bot import bot, dp
from aiogram.dispatcher.filters import Text
from russian import constants, russian, other
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import links
import database
from db import users_db


async def profile(message: types.Message):
    if users_db.have_user(message.from_user.id):
        is_premium = bool(users_db.get_is_premium(message.from_user.id))
        message.text = f'\U0001f464 *Профиль*: `{message.from_user.full_name}`   \n' \
                       f'\U00002B50 *Рейтинг*: {users_db.get_rating(message.from_user.id)}  \n' \
                       f'\U0001F4B8 *Премиум*: {"Да" if is_premium else "Нет"}\n' \
                       f'\U0001F4C2 *Обьявлении*: {len(database.get_user_ads(message.from_user.id))}'
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton(constants.premium_text, callback_data='bbb')
        markup.add(button)
        if is_premium:
            await bot.send_message(
                message.from_user.id,
                message.text,
                parse_mode='Markdown',

            )
        else:
            await bot.send_message(
                message.from_user.id,
                message.text,
                reply_markup=markup,
                parse_mode='Markdown'
            )
    else:
        await other.city_start(
            message
        )


async def buy_premium(callback: types.CallbackQuery):
    await callback.answer(
        'Premium function will be add soon',
    )


def register_next_profile(dp: Dispatcher):
    dp.register_message_handler(profile, text=links.menu_profile)
    dp.register_callback_query_handler(buy_premium, Text(equals='bbb'))


