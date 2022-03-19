from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from create_bot import bot
from db import users_db
from russian import categories, other
import links
import database


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


