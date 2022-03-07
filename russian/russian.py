from aiogram import Dispatcher, types
from create_bot import dp, bot
from links import rus_country, countryCities
from keyboards.rus_menu_kb import rus_menu_kb_button
from russian import work_with_add
from russian.work_with_add import FSMAdmin
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import users_db
import database
import links


async def menu(user_id):
    await bot.send_message(user_id, links.menu_text, reply_markup=rus_menu_kb_button)


async def rus_lang(callback: types.CallbackQuery):
    if users_db.have_user(callback.from_user.id):
        await menu(callback.from_user.id)
    else:
        await bot.send_message(callback.from_user.id, links.where_you_live_text)
    await callback.answer()


# Вывести
async def print_adds_in_cities(message: types.Message):
    await users_db.create_or_update_user(message.from_user.id, message.text)
    await bot.send_message(message.from_user.id, links.success_city)
    await menu(message.from_user.id)


async def change_city(message: types.Message):
    await bot.send_message(message.from_user.id, links.where_you_live_text)


async def work_with_data(username, user_id):
    if users_db.have_user(user_id):
        ad = users_db.get_next(user_id)
        if ad is None:
            await bot.send_message(user_id, links.no_add_in_this_city)
        else:
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(links.nxt_btn, callback_data='nxt_ad')
            b2 = InlineKeyboardButton('Хочу обменять', callback_data='like_ad ' + str(ad.get("_id")) + ' ' + str(user_id))
            markup.add(b1, b2)
            await bot.send_photo(user_id,
                                 ad.get("photo"),
                                 f'{ad.get("name")}\nОписание: {ad.get("description")}',
                                 reply_markup=markup)

    else:
        await bot.send_message(user_id, links.where_you_live_text)


async def next_ad(callback: types.CallbackQuery):
    await work_with_data(callback.from_user.username, callback.from_user.id)
    await callback.answer()


async def check_data(message: types.Message):
    await work_with_data(message.from_user.username, message.from_user.id)


async def like_ad(callback: types.CallbackQuery):
    data = callback.data.split(' ')
    ad_id, user_from_id = int(data[1]), int(data[2])
    ad = database.get_ad_by_ad_id(ad_id)
    if ad is None:
        await callback.answer(links.ad_is_deleted)
    else:
        ad_owner = database.get_ad_by_ad_id(ad_id).get('user_id')
        try:
            await bot.send_message(ad_owner, links.liked_text)
            await bot.send_photo(ad_owner,
                                 ad.get("photo"),
                                 f'{ad.get("name")}\nОписание: {ad.get("description")}',
                                 )
        except:
            users_db.make_passive(ad_owner)
        await callback.answer()


def register_step_russian(dp: Dispatcher):
    dp.register_callback_query_handler(rus_lang, text="rus_lang")
    for i in range(len(rus_country)):
        cur_list = countryCities.get(rus_country[i])
        for j in range(len(cur_list)):
            city = cur_list[j]
            dp.register_message_handler(print_adds_in_cities, text=city)

    dp.register_message_handler(work_with_add.cm_start, text='Создать обьявление')
    dp.register_message_handler(work_with_add.load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(work_with_add.load_name, state=FSMAdmin.name)
    dp.register_message_handler(work_with_add.load_description, state=FSMAdmin.description)
    dp.register_message_handler(work_with_add.my_adds, text='Мои обьявления')
    dp.register_callback_query_handler(work_with_add.next_my_add, Text(startswith="next_my_ad"))
    dp.register_callback_query_handler(work_with_add.del_my_add, Text(startswith="del_my_ad"))
    dp.register_message_handler(check_data, text='Обмен игрушками')
    dp.register_callback_query_handler(next_ad, text='nxt_ad')
    dp.register_callback_query_handler(like_ad, Text(startswith='like_ad'))
    dp.register_message_handler(change_city, text='Поменять город проживания')
