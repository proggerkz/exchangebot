from aiogram import types
from db import users_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import database
import editdistance
from create_bot import bot
import links
from russian import constants


def get_ad_by_id(ad_id, user_id):
    other_lst = users_db.get_search_list(user_id)
    search_text = ''
    cur_id = 0
    if len(other_lst) == 0:
        search_text = 'a'
    else:
        te_id = ad_id % len(other_lst)
        search_text = other_lst[len(other_lst) - 1 - te_id]
        cur_id = int(ad_id / len(other_lst))
    ads = list(database.get_all())
    lst = []
    for i in range(len(ads)):
        text = str(ads[i].get("name"))
        if len(text) > len(search_text):
            text = text[:len(ads)]
        text = text.lower()
        dist = editdistance.eval(text, search_text)
        lst.append([dist, ads[i].get("_id")])
    lst.sort()
    cur_id = cur_id % len(lst)
    for ad in ads:
        if ad.get("_id") == lst[cur_id][1]:
            return ad


def get_markup(ad_id, photo_id, search_id):
    ad = database.get_ad_by_ad_id(ad_id)
    markup = InlineKeyboardMarkup(row_width=4)
    b0text = ' '
    b3text = ' '
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
        callback_data='back_rec ' +
                      str(ad_id) + ' ' +
                      str(photo_id) + ' ' +
                      b0data + ' ' +
                      str(search_id)
    )
    b3 = InlineKeyboardButton(
        text=b3text,
        callback_data='front_rec ' +
                      str(ad_id) + ' ' +
                      str(photo_id) + ' ' +
                      b3data + ' ' +
                      str(search_id)
    )
    b1 = InlineKeyboardButton(
        text=str(photo_id + 1),
        callback_data='skip_call'
    )
    b4 = InlineKeyboardButton(
        text="Следующий",
        callback_data='next_rec ' +
                      str(ad_id) + ' ' +
                      str(search_id)
    )
    b5 = InlineKeyboardButton(
        text="Контакты",
        callback_data='contact ' +
                      ad.get("_id")
    )
    markup.add(b0, b1, b3)
    markup.add(b4, b5)
    return markup


async def back_or_front_rec(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    type_of = call_data[0]
    ad_id = call_data[1]
    photo_id = int(call_data[2])
    bdata = call_data[3]
    search_id = int(call_data[4])
    if bdata == "-1":
        await callback.answer()
    else:
        ad = database.get_ad_by_ad_id(ad_id)
        if ad is None:
            await callback.answer(links.ad_is_deleted)
        else:
            if type_of == 'front_rec':
                photo_id = photo_id + 1
            else:
                photo_id = photo_id - 1
            markup = get_markup(ad.get("_id"), photo_id, search_id)
            photo_list = ad.get('photo')
            try:
                await bot.edit_message_media(
                    chat_id=callback.from_user.id,
                    message_id=callback.message.message_id,
                    media=types.InputMediaPhoto(
                        media=photo_list[photo_id],
                        caption=f'\U0001f464 *Название*: {ad.get("name")}\n'
                                f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
                                f'\U0001F4D1 *Категория*: {ad.get("category")}/{ad.get("subcategory")}\n'
                                f'\U0001f4b0 *Цена*: {ad.get("cost")} {"тг" if str(ad.get("cost")).isnumeric() else " "}',
                        parse_mode='Markdown'
                    ),
                    reply_markup=markup
                )
            except Exception as e:
                print(e)


async def next_rec(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    ad_id = call_data[1]
    search_id = int(call_data[2])
    search_id = search_id + 1
    ad = get_ad_by_id(search_id, callback.from_user.id)
    if ad is None:
        await callback.answer(links.ad_is_deleted)
    else:
        markup = get_markup(ad.get("_id"), 0, search_id)
        await print_ad(
            callback.from_user.id,
            ad_id,
            0,
            markup
        )


async def print_ad(user_id, ad_id, photo_id, markup):
    ad = database.get_ad_by_ad_id(ad_id)
    photo_list = list(ad.get("photo"))
    await bot.send_photo(
        user_id,
        photo_list[photo_id],
        f'\U0001f464 *Название*: {ad.get("name")}\n'
        f'\U0001F4C2 *Описание*: {ad.get("description")}\n'
        f'\U0001F4D1 *Категория*: {ad.get("category")}/{ad.get("subcategory")}\n'
        f'\U0001f4b0 *Цена*: {ad.get("cost")} {"тг" if str(ad.get("cost")).isnumeric() else " "}',
        parse_mode='Markdown',
        reply_markup=markup
    )


async def recommend(message: types.Message):
    ad = get_ad_by_id(0, message.from_user.id)
    markup = get_markup(ad.get("_id"), 0, 0)
    await print_ad(message.from_user.id, ad.get("_id"), 0, markup)
