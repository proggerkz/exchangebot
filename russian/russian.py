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
from russian import work_with_add, constants, categories
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


async def chosen_category(callback: types.CallbackQuery):
    if users_db.have_user(callback.from_user.id):
        call_data = callback.data.split(' ')
        cat_id = int(call_data[1])
        sub_cat_id = int(call_data[2])
        category = categories.category_list[cat_id]
        category_list = list(categories.categories.get(category))
        category_list.sort()
        subcategory = category_list[sub_cat_id]
        ad = users_db.get_last(callback.from_user.id, subcategory)
        if ad is None:
            await bot.send_message(
                callback.from_user.id,
                links.no_add_in_this_city
            )

        else:
            markup = work_with_data(callback.from_user.id, subcategory, 0, ad.get("_id"))
            photo_list = list(ad.get('photo'))
            await bot.send_photo(
                callback.from_user.id,
                photo_list[0],
                f'\U0001f464 *Название*: {ad.get("name")}\n'
                f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
                f'\U0001F4D1 *Категория*: `{ad.get("category")}/{ad.get("subcategory")}`\n'
                f'\U0001f4b0 *Цена*: {ad.get("cost")} тг',
                reply_markup=markup,
                parse_mode='Markdown'
            )
        await callback.answer()
    else:
        await other.city_start(callback)


def work_with_data(user_id, category, photo_id, ad_id):
    ad = database.get_ad_by_ad_id(ad_id)
    markup = InlineKeyboardMarkup(row_width=4)
    b0text = ' '
    b3text = ' '
    category_id = 0
    sub_cat_id = 0
    for i in range(len(categories.category_list)):
        cat_list = list(categories.categories.get(
            categories.category_list[i]
        ))
        cat_list.sort()
        for j in range(len(cat_list)):
            if cat_list[j] == category:
                category_id = i
                sub_cat_id = j
    b0data = "-1"
    b3data = "-1"
    if photo_id != 0:
        b0text = '<<'
        b0data = "1"
    if photo_id != len(list(ad.get('photo'))) - 1:
        b3text = '>>'
        b3data = "1"
    b0 = InlineKeyboardButton(
        text=b0text,
        callback_data='back_photo ' +
                      str(category_id) + ' ' +
                      str(photo_id) + ' ' +
                      b0data + ' ' +
                      str(sub_cat_id) + ' ' +
                      str(ad.get("_id"))
    )
    b3 = InlineKeyboardButton(
        text=b3text,
        callback_data='front_photo ' +
                      str(category_id) + ' ' +
                      str(photo_id) + ' ' +
                      b3data + ' ' +
                      str(sub_cat_id) + ' ' +
                      str(ad.get("_id"))

    )
    b1 = InlineKeyboardButton(
        text=str(photo_id + 1),
        callback_data='skip_call'
    )
    b4 = InlineKeyboardButton(
        text="Следующий",
        callback_data='next_ad ' +
                      ad.get("_id") + ' ' +
                      str(category_id) + ' ' +
                      str(sub_cat_id)
    )
    b5 = InlineKeyboardButton(
        text="Контакты",
        callback_data='contact ' +
                      ad.get("_id")
    )
    markup.add(b0, b1, b3)
    markup.add(b4, b5)
    return markup


async def back_or_front(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    type_id = call_data[0]
    category_id = int(call_data[1])
    photo_id = int(call_data[2])
    do_it = call_data[3]
    sub_cat_id = int(call_data[4])
    ad_id = int(call_data[5])

    ad = database.get_ad_by_ad_id(ad_id)
    if ad is None:
        await callback.answer(links.ad_is_deleted)
    elif do_it == "-1":
        await callback.answer()
    else:
        sub_cat_list = list(
            categories.categories.get(
                categories.category_list[category_id]
            )
        )
        sub_cat_list.sort()
        sub_cat = sub_cat_list[sub_cat_id]
        if type_id == 'back_photo':
            photo_id = photo_id - 1
        else:
            photo_id = photo_id + 1
        markup = work_with_data(
            callback.from_user.id,
            sub_cat,
            photo_id,
            ad.get("_id")
        )
        photo_list = list(ad.get('photo'))

        msg_id = callback.message.message_id
        try:
            await bot.edit_message_media(
                chat_id=callback.from_user.id,
                message_id=msg_id,
                media=types.InputMediaPhoto(
                    media=photo_list[photo_id],
                    caption=f'\U0001f464 *Название*: {ad.get("name")}\n'
                            f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
                            f'\U0001F4D1 *Категория*: `{ad.get("category")}/{ad.get("subcategory")}`\n'
                            f'\U0001f4b0 *Цена*: {ad.get("cost")} тг',
                    parse_mode='Markdown'

                ),
                reply_markup=markup,
            )
        except:
            await bot.send_message(
                callback.from_user.id,
                'Попробуйте нажать /start и зайдите в поиск обратно'
            )


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


def get_subcategory(page, category, msg_id):
    sub_cat_list = list(categories.categories.get(category))
    sub_cat_list.sort()
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
        callback_data='nxt_sub_cat ' + str(page) + ' ' + str(msg_id) + ' ' + str(cat_id)
    )
    b2 = InlineKeyboardButton(
        text='Предыдуший',
        callback_data='prev_sub_cat ' + str(page) + ' ' + str(msg_id) + ' ' + str(cat_id)
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


def get_cat_name(category_id, subcategory_id):
    cat_list = list(categories.categories.get(
        categories.category_list[category_id]
    ))
    cat_list.sort()
    return cat_list[subcategory_id]


async def next_cat_ad(callback: types.CallbackQuery):
    user_city = users_db.get_city_of_user(callback.from_user.id)
    call_data = callback.data.split(' ')
    ad_id = call_data[1]
    cat_id = int(call_data[2])
    sub_cat_id = int(call_data[3])
    subcategory = get_cat_name(cat_id, sub_cat_id)
    ads = database.get_city_ads(user_city, subcategory)
    if len(ads) == 0:
        await callback.answer(links.no_add_in_this_city)
    else:
        _id = len(ads) - 1
        for i in range(len(ads)):
            cur_ad_id = ads[i].get("_id")
            if cur_ad_id < ad_id:
                _id = i
        markup = work_with_data(
            callback.from_user.id,
            subcategory,
            0,
            ads[_id].get("_id")
        )
        ad = ads[_id]
        photo_list = ad.get('photo')
        await bot.send_photo(
            callback.from_user.id,
            photo_list[0],
            f'\U0001f464 *Название*: {ad.get("name")}\n'
            f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
            f'\U0001F4D1 *Категория*: `{ad.get("category")}/{ad.get("subcategory")}`\n'
            f'\U0001F4B0 *Цена*: {ad.get("cost")} тг\n',
            reply_markup=markup,
            parse_mode='Markdown'
        )


async def next_or_prev_sub_category(callback: types.CallbackQuery):
    print('I am here')
    call_data = callback.data.split(' ')
    page_id = int(call_data[1])
    msg_id = int(call_data[2])
    cat_id = int(call_data[3])
    if call_data[0] == 'nxt_sub_cat':
        page_id = page_id + 1
    else:
        page_id = page_id - 1
    markup = get_subcategory(page_id, categories.category_list[cat_id], 0)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=constants.cat_text,
        reply_markup=markup
    )


async def category_menu(message: types.Message):
    category = message.text
    markup = get_subcategory(0, category, message.message_id)
    await bot.send_message(
        message.from_user.id,
        constants.cat_text,
        reply_markup=markup,
    )


async def contact(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    ad_id = call_data[1]
    ad = database.get_ad_by_ad_id(ad_id)
    if ad is None:
        await callback.answer(links.ad_is_deleted)
    else:
        await bot.send_message(
            callback.from_user.id,
            f'*Контакты пользователя*: \n'
            f'\U0001f4f1 Номер телефона: {ad.get("phone")}\n'
            f'\U00002714 Телеграм: @{ad.get("username")}',
            parse_mode='Markdown'
        )
        await callback.answer()


def register_step_russian(dp: Dispatcher):
    # Russian
    dp.register_callback_query_handler(rus_lang, text="rus_lang")
    dp.register_message_handler(go_to_menu, text=constants.menu_text)
    dp.register_message_handler(next_or_prev, text=constants.next_btn)
    dp.register_message_handler(next_or_prev, text=constants.prev_btn)
    dp.register_callback_query_handler(next_or_prev_sub_category, Text(startswith='nxt_sub_cat'))
    dp.register_callback_query_handler(next_or_prev_sub_category, Text(startswith='prev_sub_cat'))
    dp.register_callback_query_handler(contact, Text(startswith='contact'))
    dp.register_message_handler(check_data, text=links.menu_exchange)
    for i in range(len(categories.category_list)):
        dp.register_message_handler(
            category_menu,
            text=categories.category_list[i]
        )
    dp.register_callback_query_handler(next_cat_ad, Text(startswith='next_ad'))
    dp.register_callback_query_handler(back_or_front, Text(startswith='back_photo'))
    dp.register_callback_query_handler(back_or_front, Text(startswith='front_photo'))
    dp.register_callback_query_handler(chosen_category, Text(startswith='sub_cat'))

    # Work with add
    # Начать создать обьявление
    dp.register_message_handler(work_with_add.cm_start, text=links.menu_create)
    # Отмена создания
    dp.register_message_handler(work_with_add.cancel_handler, text=constants.cancel_text, state='*')
    dp.register_message_handler(work_with_add.load_category, state=FSMAdmin.category)
    dp.register_callback_query_handler(work_with_add.load_subcategory, state=FSMAdmin.subcategory)
    dp.register_message_handler(work_with_add.skip, text=constants.skip_text, state=FSMAdmin.photo)
    dp.register_message_handler(work_with_add.load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(work_with_add.load_phone_number, state=FSMAdmin.phone)
    dp.register_message_handler(work_with_add.load_name, state=FSMAdmin.name)
    dp.register_message_handler(work_with_add.load_description, state=FSMAdmin.description)
    dp.register_message_handler(work_with_add.load_cost, state=FSMAdmin.price)
    dp.register_message_handler(work_with_add.my_adds, text=links.menu_my_ads)
    dp.register_callback_query_handler(work_with_add.next_my_add, Text(startswith="next_my_ad"))
    dp.register_callback_query_handler(work_with_add.del_my_add, Text(startswith="del_my_ad"))


