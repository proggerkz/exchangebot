from aiogram import types
from russian import russian, constants
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from create_bot import bot
from db import users_db
from aiogram.dispatcher.filters.state import State, StatesGroup
import links
import database
from keyboards.category import category_btn_with_cancel
from keyboards.cancel_kb import cancel_kb
from keyboards.rus_menu_kb import rus_menu_kb_button


class FSMAdmin(StatesGroup):
    category = State()
    photo = State()
    name = State()
    description = State()


async def cm_start(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await FSMAdmin.category.set()
        await message.reply(links.create_add_text, reply_markup=category_btn_with_cancel)
    else:
        await russian.change_city(message)


async def cancel_handler(message: types.Message, state: FSMContext):
    if users_db.have_user(message.from_user.id):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply(constants.success_cancel)
        await russian.menu(message.from_user.id)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton(text=links.menu_change_city)
        markup.add(button)
        await state.finish()
        await bot.send_message(message.from_user.id,
                               constants.to_use_text,
                               reply_markup=markup)


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text not in links.category:
            await bot.send_message(message.from_user.id, links.choose_right_category)
        else:
            data['category'] = message.text
            await FSMAdmin.next()
            await message.reply(constants.download_photo, reply_markup=cancel_kb)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply(constants.download_name, reply_markup=cancel_kb)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply(constants.download_description, reply_markup=cancel_kb)


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data['user_id'] = message.from_user.id
        data['city'] = users_db.get_city_of_user(message.from_user.id)
    await database.ad_add_moderator(state)
    await message.answer(constants.success_download, reply_markup=rus_menu_kb_button)
    await state.finish()


async def create_markup_and_send_message(el, user_id):
    print('here i ami am')
    print(el)
    markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text=links.nxt_btn, callback_data="next_my_ad " + el.get("_id"))
    b2 = InlineKeyboardButton(text=links.del_btn, callback_data="del_my_ad " + el.get("_id"))
    markup.add(b1, b2)
    await bot.send_photo(
        user_id,
        el.get("photo"),
        f'{el.get("name")}\nОписание игрушки: {el.get("description")}',
        reply_markup=markup
    )


async def my_adds(message: types.Message):
    if users_db.have_user(message.from_user.id):
        cur_db = database.get_user_ads(message.from_user.id)
        if len(cur_db) == 0:
            await bot.send_message(message.from_user.id, links.no_add_text)
        else:
            await create_markup_and_send_message(cur_db[0], message.from_user.id)
    else:
        await russian.change_city(message)


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
        await create_markup_and_send_message(cur_db[id_of_last], callback.from_user.id)
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


