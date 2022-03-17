from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from create_bot import bot, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import links
import database
from russian import other
from db import users_db
from keyboards.cancel_kb import cancel_kb
from aiogram import types
from russian import constants
from russian import russian


class Search(StatesGroup):
    text = State()


async def search_start(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await Search.text.set()
        await message.reply(
            constants.search_text,
            reply_markup=cancel_kb
        )
    else:
        await other.city_start(message)


async def load_text(message: types.Message, state: FSMContext):
    search_text = message.text
    await state.finish()
    await russian.menu(message.from_user.id)
    await message.reply(
        search_text
    )


async def next_or_prev_mine(callback: types.CallbackQuery):
    call_data = callback.data.split(' ')
    type_id = call_data[0]
    ad_id = call_data[1]
    photo_id = int(call_data[2])
    bdata = call_data[3]
    if bdata == '-1':
        await callback.answer()
    else:
        ad = database.get_ad_by_ad_id(ad_id)
        if type_id == 'prev_mine':
            photo_id = photo_id - 1
        else:
            photo_id = photo_id + 1
        photo_list = list(ad.get('photo'))
        msg_id = callback.message.message_id
        markup = InlineKeyboardMarkup(row_width=3)
        b1 = InlineKeyboardButton(text=links.nxt_btn, callback_data="next_my_ad " + ad_id)
        b2 = InlineKeyboardButton(text=links.del_btn, callback_data="del_my_ad " + ad_id)
        photo_list = list(ad.get('photo'))
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
            callback_data='prev_mine ' + ad_id + ' ' + str(photo_id) + ' ' + b0data
        )

        by = InlineKeyboardButton(
            text=str(photo_id + 1),
            callback_data='skip_call'
        )

        bz = InlineKeyboardButton(
            text=b3text,
            callback_data='next_mine ' + ad_id + ' ' + str(photo_id) + ' ' + b3data
        )
        markup.add(bx, by, bz)
        markup.add(b1, b2)
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
            print("Bad")
def register_next_search(dp: Dispatcher):
    dp.register_message_handler(search_start, text=links.menu_search)
    dp.register_message_handler(load_text, state=Search.text)
    dp.register_callback_query_handler(next_or_prev_mine, Text(startswith='next_mine'))
    dp.register_callback_query_handler(next_or_prev_mine, Text(startswith='prev_mine'))