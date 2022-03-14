import database
import links
from db import rated
from russian import other
from keyboards.rus_menu_kb import rus_menu_kb_button
from db import users_db
from db import liked_ads
from aiogram.dispatcher import Dispatcher
from russian import constants
from create_bot import bot
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
                call_data = 'exc_us ' + str(user_to_id) + ' ' + str(ad_id) + ' ' + ads_of_user[i].get(
                    "_id") + ' ' + username
                print(call_data)
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
        await callback.answer('Участнику отправлено запрос об обмене')


async def my_liked_contact(message: types.Message):
    if users_db.have_user(message.from_user.id):
        connect = liked_ads.get_my_ad(message.from_user.id)
        if connect is None:
            await bot.send_message(message.from_user.id, constants.no_liked_text)
        else:
            ad_from = database.get_ad_by_ad_id(connect.get('ad_from_id'))
            ad_to = database.get_ad_by_ad_id(connect.get('ad_to_id'))
            markup = InlineKeyboardMarkup()
            text = str(connect.get('user_from_id')) + ' ' + str(connect.get('user_to_id')) + ' ' \
                   + str(connect.get('ad_from_id')) + ' ' + str(connect.get('ad_to_id')) + ' ' + str(
                connect.get('username'))
            b1 = InlineKeyboardButton('Я согласен', callback_data=f'accept 1 {text}')
            b2 = InlineKeyboardButton('Я не согласен', callback_data=f'accept -1 {text}')
            markup.add(b1, b2)
            await bot.send_photo(
                message.from_user.id,
                ad_from.get('photo'),
                f'Один из участников хочет поменять игру на вашу игру: '
                f'*{ad_to.get("name")}*\n\n'
                f'Данные его игрушки:\n'
                f'\U0001f464 *Название*: {ad_from.get("name")}\n'
                f'\U0001F4C2 *Описание*: {ad_from.get("description")}\n'
                f'\U0001F4D1 *Категория*: {ad_from.get("category")}\n'
                f'\U00002B50 *Рейтинг пользователя*: {users_db.get_rating(ad_from.get("user_id"))}\n'
                f'Если вам тоже понравилась игра и хотите обменять то я могу дать контакты хозяина',
                reply_markup=markup,
                parse_mode='Markdown'
            )

    else:
        await other.city_start(message)


async def acceptance(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    acc = call_data[1]

    user_from_id, user_to_id = int(call_data[2]), int(call_data[3])
    ad_from_id, ad_to_id = int(call_data[4]), int(call_data[5])
    username = call_data[6]
    if liked_ads.have_connection(user_from_id, user_to_id, ad_from_id, ad_to_id) is None:
        await callback.answer(constants.deleted_connection)
    else:
        ad_from = database.get_ad_by_ad_id(ad_from_id)
        ad_to = database.get_ad_by_ad_id(ad_to_id)
        if ad_from is None:
            await callback.answer(constants.ad_to_deleted)
        elif ad_to is None:
            await callback.answer(constants.deleted_myself)
        else:
            if acc == "-1":
                await callback.answer()
                await my_liked_contact(callback)
            else:
                await bot.send_photo(callback.from_user.id,
                                     ad_to.get('photo'),
                                     f'Я хочу обменять мою игру на вашу игру которую вы раньше лайкнули под названием: '
                                     f'*{ad_from.get("name")}*\n\n'
                                     f'\U0001f464 *Название*: {ad_to.get("name")}\n'
                                     f'\U0001F4C2 *Описание*: {ad_to.get("description")}\n'
                                     f'\U0001F4D1 *Категория*: {ad_to.get("category")}\n'
                                     f'\U00002B50 *Мой рейтинг*: {users_db.get_rating(callback.from_user.id)}\n',
                                     parse_mode='Markdown'
                                     )
                await bot.send_message(
                    callback.from_user.id,
                    'Отправьте сообщение выше участнику по нику: @' + username,
                    reply_markup=rus_menu_kb_button
                )
                await callback.answer()
                if rated.have_connection(callback.from_user.id, user_from_id) is None:
                    mrk = InlineKeyboardMarkup(row_width=5)
                    for i in range(5):
                        btn = InlineKeyboardButton(
                            text=str(i + 1),
                            callback_data='rate ' + str(i + 1) + ' ' + str(user_from_id)
                        )
                        mrk.insert(btn)
                    await bot.send_message(
                        callback.from_user.id,
                        'Если вы уже встретились и обменяли свои игрушки вы можете оценить участника по состоянию '
                        'игрушки и по обращению обладателем игрушки для обмена',
                        reply_markup=mrk
                    )
            liked_ads.delete_connection(
                int(user_from_id),
                int(user_to_id),
                int(ad_from_id),
                int(ad_to_id)
            )


async def rate_user(callback: types.CallbackQuery):
    lst = callback.data.split(' ')
    rating = int(lst[1])
    user_from = int(lst[2])
    if rated.have_connection(callback.from_user.id, user_from) is None:
        rated.change_rating(callback.from_user.id, user_from, rating)
        await callback.answer()
    else:
        await callback.answer('Вы оценили этого участника раньше')


def register_next_connection(dp: Dispatcher):
    dp.register_callback_query_handler(chosen_ad_exchange, Text(startswith='exc_us'))
    dp.register_message_handler(my_liked_contact, text=constants.wanna_see)
    dp.register_message_handler(my_liked_contact, text=links.menu_my_liked)
    dp.register_callback_query_handler(acceptance, Text(startswith='accept'))
    dp.register_callback_query_handler(rate_user, Text(startswith='rate'))

