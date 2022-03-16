from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import database
import links
from russian import other
from create_bot import bot, dp
from db import users_db
from keyboards.rus_menu_kb import rus_menu_kb_button
from russian import work_with_add, constants, connection, categories
from russian.work_with_add import FSMAdmin


async def menu(user_id):
    await bot.send_message(
        user_id,
        links.menu_text,
        reply_markup=rus_menu_kb_button
    )


async def rus_lang(callback: types.CallbackQuery):
    if users_db.have_user(callback.from_user.id):
        await menu(callback.from_user.id)
    else:
        await bot.send_message(
            callback.from_user.id,
            links.where_you_live_text
        )
    await callback.answer()


# Вывести
async def print_adds_in_cities(message: types.Message):
    message.text = message.text.upper()
    await users_db.create_or_update_user(message.from_user.id, message.text)
    await bot.send_message(
        message.from_user.id,
        links.success_city
    )
    await menu(message.from_user.id)


async def change_city(message: types.Message):
    await bot.send_message(message.from_user.id, links.where_you_live_text)


async def chosen_category(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await menu(message.from_user.id)
        await work_with_data(message.from_user.id, message.text)
    else:
        await other.city_start(message)


async def work_with_data(user_id, category_id):
    ad = users_db.get_next(user_id, category_id)
    if ad is None:
        await bot.send_message(user_id, links.no_add_in_this_city)
    else:
        markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(links.nxt_btn, callback_data='nxt_ad ' + category_id)
        b2 = InlineKeyboardButton(constants.wanna_change,
                                  callback_data='like_ad ' + str(ad.get("_id")) + ' ' + str(user_id))
        markup.add(b1, b2)
        await bot.send_photo(
            user_id,
            ad.get("photo"),
            f'\U0001f464 *Название*: {ad.get("name")}\n'
            f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
            f'\U0001F4D1 *Категория*: {ad.get("category")}\n'
            f'\U00002B50 *Рейтинг пользователя*: {users_db.get_rating(ad.get("user_id"))}',
            reply_markup=markup,
            parse_mode='Markdown'
        )


async def next_ad(callback: types.CallbackQuery):
    data = callback.data[7:]
    await work_with_data(callback.from_user.id, data)
    await callback.answer()


def get_category(page):
    cur_page = page
    cat_keys = list(categories.categories.keys())
    if cur_page * 5 > len(cat_keys):
        cur_page = 1
    if cur_page < 0:
        cur_page = 0
    markup = ReplyKeyboardMarkup()
    start_id = cur_page * 5
    end_id = min(cur_page * 5 + 5, len(cat_keys))
    for i in range(start_id, end_id):
        button = KeyboardButton(cat_keys[i])
        if (i - start_id) % 2 == 0:
            markup.add(button)
        else:
            markup.insert(button)
    btn1 = KeyboardButton(constants.next_btn)
    btn2 = KeyboardButton(constants.prev_btn)
    if cur_page != 0:
        if cur_page * 5 + 5 < len(cat_keys):
            markup.insert(btn1)
            markup.add(btn2)
        else:
            markup.insert(btn2)
    else:
        markup.insert(btn1)
    return markup


def get_subcategory(page, category):
    sub_cat_list = list(categories.categories.get(category))
    markup = InlineKeyboardMarkup()
    cat_id = 0
    for i in range(len(categories.category_list)):
        if categories.category_list[i] == category:
            cat_id = i
    for i in range(page * 7, min(page * 7 + 7, len(sub_cat_list))):
        button = InlineKeyboardButton(
            text=sub_cat_list[i],
            callback_data="sub_cat " + str(cat_id) + ' ' + str(i)
        )
        markup.add(button)
    b1 = InlineKeyboardButton(
        text='Следующий',
        callback_data='nxt_sub_cat'
    )
    b2 = InlineKeyboardButton(
        text='Предыдуший',
        callback_data='prev_sub_cat'
    )
    if page != 0:
        if page * 7 + 7 < len(sub_cat_list):
            markup.add(b2, b1)
        else:
            markup.add(b2)
    elif page * 7 + 7 < len(sub_cat_list):
        markup.add(b1)
    return markup


async def check_data(message: types.Message):
    if users_db.have_user(message.from_user.id):
        markup = get_category(0)
        btn = KeyboardButton(constants.menu_text)
        markup.add(btn)
        await bot.send_message(
            message.from_user.id,
            links.menu_text,
            reply_markup=markup
        )
        users_db.change_category(
            message.from_user.id,
            message.text,
            0
        )
    else:
        await other.city_start(message)


async def go_to_menu(message: types.Message):
    await menu(message.from_user.id)


async def like_ad(callback: types.CallbackQuery):
    if len(database.get_user_ads(callback.from_user.id)) != 0:
        data = callback.data.split(' ')
        ad_id, user_from_id = int(data[1]), int(data[2])
        ad = database.get_ad_by_ad_id(ad_id)
        if ad is None:
            await callback.answer(links.ad_is_deleted)
        else:
            ad_owner = database.get_ad_by_ad_id(ad_id).get('user_id')
            if ad_owner != user_from_id:
                await connection.make_connection(callback.from_user.id, ad_owner, ad_id, 0, callback.from_user.username)
                await callback.answer()
            else:
                await callback.answer(constants.owners_add)
    else:
        await callback.answer(links.no_user_ad_text)


async def next_or_prev(message: types.Message):
    if users_db.have_user(message.from_user.id):
        last_category = users_db.last_category(message.from_user.id)
        cat_keys = list(categories.categories.keys())
        if last_category[0] == links.menu_exchange:
            lst = last_category[1]
            if message.text == constants.next_btn:
                lst = lst + 1
                if lst * 5 >= len(cat_keys):
                    lst -= 1
                markup = get_category(lst)
                btn = KeyboardButton(constants.menu_text)
                markup.add(btn)
                await bot.send_message(
                    message.from_user.id,
                    links.choose_right_category,
                    reply_markup=markup
                )
                users_db.change_category(
                    message.from_user.id,
                    last_category[0],
                    lst
                )
            else:
                lst = lst - 1
                lst = max(lst, 0)
                markup = get_category(lst)
                btn = KeyboardButton(constants.menu_text)
                markup.add(btn)
                await bot.send_message(
                    message.from_user.id,
                    links.choose_right_category,
                    reply_markup=markup
                )
                users_db.change_category(
                    message.from_user.id,
                    last_category[0],
                    lst
                )
    else:
        await other.city_start(message)


async def category_menu(message: types.Message):
    category = message.text
    markup = get_subcategory(0, category)
    await bot.send_message(
        message.from_user.id,
        constants.cat_text,
        reply_markup=markup,
    )



def register_step_russian(dp: Dispatcher):
    dp.register_callback_query_handler(rus_lang, text="rus_lang")
    dp.register_message_handler(go_to_menu, text=constants.menu_text)
    dp.register_message_handler(next_or_prev, text=constants.next_btn)
    dp.register_message_handler(next_or_prev, text=constants.prev_btn)
    dp.register_message_handler(work_with_add.cm_start, text=links.menu_create)
    dp.register_message_handler(work_with_add.cancel_handler, text=constants.cancel_text, state='*')
    dp.register_message_handler(work_with_add.type_city, state=FSMAdmin.type)
    dp.register_message_handler(work_with_add.load_category, state=FSMAdmin.category)
    dp.register_message_handler(work_with_add.skip, text=constants.skip_text,state=FSMAdmin.photo)
    dp.register_message_handler(work_with_add.load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(work_with_add.load_name, state=FSMAdmin.name)
    dp.register_message_handler(work_with_add.load_description, state=FSMAdmin.description)
    dp.register_message_handler(work_with_add.load_cost, state=FSMAdmin.price)
    dp.register_message_handler(work_with_add.my_adds, text=links.menu_my_ads)
    dp.register_callback_query_handler(work_with_add.next_my_add, Text(startswith="next_my_ad"))
    dp.register_callback_query_handler(work_with_add.del_my_add, Text(startswith="del_my_ad"))
    dp.register_message_handler(check_data, text=links.menu_exchange)

    for i in range(len(categories.category_list)):
        dp.register_message_handler(
            category_menu,
            text=categories.category_list[i]
        )
    dp.register_callback_query_handler(next_ad, Text(startswith='nxt_ad'))
    dp.register_callback_query_handler(like_ad, Text(startswith='like_ad'))
