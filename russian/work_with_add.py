from aiogram import types
from russian import russian, constants
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from create_bot import bot
from db import users_db
from russian import categories, other
from aiogram.dispatcher.filters.state import State, StatesGroup
import links
import database
from keyboards.skip import skip_btn
from keyboards.cancel_kb import cancel_kb
from keyboards.rus_menu_kb import rus_menu_kb_button
from keyboards.cost import cost_kb

class FSMAdmin(StatesGroup):
    category = State()
    subcategory = State()
    photo = State()
    phone = State()
    name = State()
    description = State()
    price = State()


async def cm_start(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await FSMAdmin.category.set()
        markup = russian.get_category(0)
        btn = KeyboardButton(constants.cancel_text)
        markup.add(btn)
        await message.reply(
            links.create_add_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    else:
        await other.city_start(message)


async def cancel_handler(message: types.Message, state: FSMContext):
    if users_db.have_user(message.from_user.id):
        current_state = await state.get_state()
        if current_state is None:
            await russian.menu(message.from_user.id)
            return
        await state.finish()
        await message.reply(constants.success_cancel)
        await russian.menu(message.from_user.id)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton(text=links.menu_change_city)
        markup.add(button)
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            constants.to_use_text,
            reply_markup=markup
        )


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "category_id" not in data.keys():
            data["category_id"] = 0
        cat_len = len(list(categories.categories))
        if message.text not in categories.categories.keys():
            if message.text == constants.next_btn:
                data['category_id'] += 1
                if data['category_id'] * 5 >= cat_len:
                    data['category_id'] -= 1
                markup = russian.get_category(data['category_id'])
                btn = KeyboardButton(constants.cancel_text)
                markup.add(btn)
                await message.reply(
                    links.choose_right_category,
                    reply_markup=markup
                )
            elif message.text == constants.prev_btn:
                if data['category_id'] != 0:
                    data['category_id'] -= 1
                markup = russian.get_category(data['category_id'])
                btn = KeyboardButton(constants.cancel_text)
                markup.add(btn)
                await message.reply(
                    links.choose_right_category,
                    reply_markup=markup
                )
            else:
                await bot.send_message(message.from_user.id, links.choose_right_category)
        else:
            data['category'] = message.text
            await FSMAdmin.next()
            markup = russian.get_subcategory(0, message.text, 0)
            await bot.send_message(
                message.from_user.id,
                'ОК',
                reply_markup=cancel_kb
            )
            await message.reply(
                links.choose_right_category,
                reply_markup=markup
            )


async def load_subcategory(callback: types.CallbackQuery, state=FSMContext):
    type_call = callback.data.split(' ')
    if type_call[0] == 'sub_cat':
        cat_id = int(type_call[1])
        data_cat = ''
        async with state.proxy() as data:
            data_cat = data['category']
        cat_cur_id = 0
        for i in range(len(categories.category_list)):
            if categories.category_list[i] == data_cat:
                cat_cur_id = i
        if cat_cur_id != cat_id:
            await callback.answer(
                'Кажется вы данное время в создании обьявления'
            )
        else:
            category = categories.category_list[cat_id]
            sub_cat_list = list(categories.categories.get(category))
            sub_cat_list.sort()
            sub_cat_id = int(type_call[2])
            async with state.proxy() as data:
                data['subcategory'] = sub_cat_list[sub_cat_id]
            await FSMAdmin.next()
            await callback.message.reply(
                constants.download_photo,
                reply_markup=cancel_kb
            )
            await callback.answer()
    elif type_call[0] == 'prev_sub_cat' or type_call[0] == 'nxt_sub_cat':
        page_id = int(type_call[1])
        msg_id = int(type_call[2])
        cat_id = int(type_call[3])
        data_cat = ''
        async with state.proxy() as data:
            data_cat = data['category']
        cat_cur_id = 0
        for i in range(len(categories.category_list)):
            if categories.category_list[i] == data_cat:
                cat_cur_id = i
        if cat_cur_id != cat_id:
            await callback.answer(
                'Кажется вы данное время в создании обьявления'
            )
        else:
            if type_call[0] == 'prev_sub_cat':
                page_id = page_id - 1
            else:
                page_id = page_id + 1
            markup = russian.get_subcategory(page_id, categories.category_list[cat_id], msg_id)
            await bot.edit_message_text(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                text=links.choose_right_category,
                reply_markup=markup
            )
    else:
        await callback.answer(constants.create_or_cancel)


async def skip(message: types.Message, state: FSMContext):
    await FSMAdmin.next()
    await message.reply(
        constants.write_phone,
        reply_markup=cancel_kb
    )


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'photo' not in data.keys():
            data['photo'] = []
        data['photo'].append(message.photo[0].file_id)

        if len(data['photo']) == 9:
            await FSMAdmin.next()
            await message.reply(
                constants.write_phone,
                reply_markup=cancel_kb
            )
        else:
            await message.reply(
                constants.new_or_skip,
                reply_markup=skip_btn
            )


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await FSMAdmin.next()
    await message.reply(
        constants.download_name
    )


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply(
        constants.download_description,
        reply_markup=cancel_kb
    )


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data['user_id'] = message.from_user.id
        data['city'] = users_db.get_city_of_user(message.from_user.id)
        data['username'] = message.from_user.username
    await message.reply(
            constants.how_much_photo,
            reply_markup=cost_kb
        )
    await FSMAdmin.next()


async def load_cost(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        async with state.proxy() as data:
            data['cost'] = int(message.text)
        await database.ad_add_moderator(state)
        await message.reply(
            constants.success_download,
            reply_markup=rus_menu_kb_button
        )
        await state.finish()
    elif message.text == constants.free_text or message.text == constants.equalize_text:
        async with state.proxy() as data:
            data['cost'] = message.text
        await database.ad_add_moderator(state)
        await message.reply(
            constants.success_download,
            reply_markup=rus_menu_kb_button
        )
        await state.finish()
    else:
        await message.reply(
            constants.numeric_text
        )


async def create_markup_and_send_message(el, user_id, photo_id):
    markup = InlineKeyboardMarkup(row_width=3)
    b1 = InlineKeyboardButton(text=links.nxt_btn, callback_data="next_my_ad " + el.get("_id"))
    b2 = InlineKeyboardButton(text=links.del_btn, callback_data="del_my_ad " + el.get("_id"))
    photo_list = list(el.get('photo'))
    b0data = "-1"
    b3data = "-1"
    b0text = ' '
    b3text = ' '
    if photo_id != 0:
        b0text = '<<'
        b0data = "1"
    if photo_id != len(list(photo_list)) - 1:
        b3text = '>>'
        b3data = "1"
    bx = InlineKeyboardButton(
        text=b0text,
        callback_data='prev_mine ' + el.get("_id") + ' ' + str(photo_id) + ' ' + b0data
    )

    by = InlineKeyboardButton(
        text=str(photo_id + 1),
        callback_data='skip_call'
    )

    bz = InlineKeyboardButton(
        text=b3text,
        callback_data='next_mine ' + el.get("_id") + ' ' + str(photo_id) + ' ' + b3data
    )
    markup.add(bx, by, bz)
    markup.add(b1, b2)
    await bot.send_photo(
        user_id,
        photo_list[photo_id],
        f'\U0001f464 *Название*: {el.get("name")}\n'
        f'\U0001F4C2 *Описание*: {el.get("description")}\n'
        f'\U0001F4D1 *Категория*: {el.get("category")}/{el.get("subcategory")}\n'
        f'\U0001f4b0 *Цена*: {el.get("cost")} {"тг" if str(el.get("cost")).isnumeric() else " "}',
        reply_markup=markup,
        parse_mode='Markdown'
    )


async def my_adds(message: types.Message):
    if users_db.have_user(message.from_user.id):
        cur_db = database.get_user_ads(message.from_user.id)
        if len(cur_db) == 0:
            await bot.send_message(message.from_user.id, links.no_add_text)
        else:
            await create_markup_and_send_message(cur_db[0], message.from_user.id, 0)
    else:
        await other.city_start(message)


async def next_my_add(callback: types.CallbackQuery):
    t = callback.data.split(' ')
    cur_db = database.get_user_ads(callback.from_user.id)
    last_id = int(t[1])
    id_of_last = -1
    for i in range(len(cur_db)):
        if int(cur_db[i].get("_id")) == last_id:
            id_of_last = i
    if id_of_last == -1:
        await callback.answer(links.add_has_been_delete)
    else:
        id_of_last += 1
        id_of_last %= len(cur_db)
        await create_markup_and_send_message(cur_db[id_of_last], callback.from_user.id, 0)
        await callback.answer()


async def del_my_add(callback: types.CallbackQuery):
    t = callback.data.split(' ')
    cur_db = database.get_user_ads(callback.from_user.id)
    id_of_last = -1
    for i in range(len(cur_db)):
        if int(cur_db[i].get("_id")) == int(t[1]):
            id_of_last = i
            break
    if id_of_last == -1:
        await callback.answer(links.add_has_been_delete)
    else:
        database.delete_add_ads(t[1])
        await callback.answer(links.success_delete)


