import database
import links
from db import users_db
from db import liked_ads
from aiogram.dispatcher import Dispatcher
from russian import constants
from create_bot import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


async def make_connection(user_from_id, user_to_id, ad_id, page, username):
    ads_of_user = database.get_user_ads(user_from_id)
    if len(ads_of_user) == 0:
        await bot.send_message(user_from_id, links.no_user_ad_text)
    else:
        if page * 5 >= len(ads_of_user):
            await bot.send_message(user_from_id, constants.no_more_page)
        else:
            cur_id = page * 5
            markup = InlineKeyboardMarkup()
            for i in range(min(cur_id + 5, len(ads_of_user))):
                call_data = 'exc_us ' + str(user_to_id) + ' ' + str(ad_id) + ' ' + ads_of_user[i].get("_id") + ' ' + username
                button = InlineKeyboardButton(text=ads_of_user[i].get('name'), callback_data=call_data)
                markup.add(button)

            await bot.send_message(user_from_id, constants.which_ad_send, reply_markup=markup)


async def chosen_ad_exchange(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    user_from_id = callback.from_user.id
    user_to_id = int(call_data[1])
    ad_from_id = int(call_data[3])
    ad_to_id = int(call_data[2])
    username_from = call_data[4]
    ad_from = database.get_ad_by_ad_id(ad_from_id)
    ad_to = database.get_ad_by_ad_id(ad_to_id)
    if ad_from is None:
        await callback.answer(constants.ad_from_deleted)
    elif ad_to is None:
        await callback.answer(constants.ad_to_deleted)
    elif liked_ads.have_connection(user_from_id, user_to_id, ad_from_id, ad_to_id):
        await callback.answer(constants.already_liked)
    else:
        liked_ads.create_data(user_from_id, user_to_id, ad_from_id, ad_to_id, username_from)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton(constants.wanna_see)
        button2 = KeyboardButton(constants.menu_text)
        markup.add(button1, button2)
        try:
            await bot.send_message(user_to_id,
                                   constants.liked_text,
                                   reply_markup=markup)
        except:
            users_db.make_passive(user_to_id)


async def my_liked_contact(message: types.Message):
    connect = liked_ads.get_my_ad(message.from_user.id)
    ad_from = database.get_ad_by_ad_id(connect.get('ad_from_id'))
    ad_to = database.get_ad_by_ad_id(connect.get('ad_to_id'))
    markup = InlineKeyboardMarkup()
    text = str(connect.get('user_from_id')) + ' ' + str(connect.get('user_to_id')) + ' ' \
           + str(connect.get('ad_from_id')) + ' ' + connect.get('ad_to_id')
    b1 = InlineKeyboardButton('Я согласен', callback_data=f'accept 1 {text}')
    b2 = InlineKeyboardButton('Я не согласен', callback_data=f'accept -1 {text}')
    markup.add(b1, b2)
    await bot.send_photo(message.from_user.id,
                         ad_from.get('photo'),
                         f'Один из участников хочет поменять игру на вашу игру'
                         f'{ad_to.get("name")}\n\n'
                         f'Данные его игрушки: '
                         f'Название: {ad_from.get("name")}'
                         f'Категория: {ad_from.get("category")}'
                         f'Описание: {ad_from.get("description")}'
                         f'Если понравилась вы тоже хотите обменять я дам его контакты',
                         reply_markup=markup)


def register_next_connection(dp: Dispatcher):
    dp.register_callback_query_handler(chosen_ad_exchange, Text(startswith='exc_us'))
    dp.register_message_handler(my_liked_contact, text=constants.wanna_see)
    # dp.register_callback_query_handler(acceptance, Text(startswith='accept'))

