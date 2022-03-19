from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from russian import constants, russian
from db import users_db
from aiogram import types
import links
from cities import cities


class CityOfUser(StatesGroup):
    city = State()



async def city_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(constants.cancel_text)
    markup.add(button)
    await CityOfUser.city.set()
    await bot.send_message(message.from_user.id, links.where_you_live_text, reply_markup=markup)


def lcs(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]

async def city_name(message: types.Message, state: FSMContext):
    city = str(message.text)
    city = city.lower()
    city_list = []
    for i in range(len(cities)):
        cur_city = cities[i]
        name_city = str(cur_city.split('(')[0])
        if len(name_city) > len(city):
            name_city = name_city[:len(city)]
        name_city = name_city.lower()
        dist = lcs(name_city, city)
        st = [dist, cur_city, i]
        city_list.append(st)

    city_list.sort(reverse=True)
    markup = InlineKeyboardMarkup()
    for i in range(5):
        city_btn = InlineKeyboardButton(text=city_list[i][1],
                                        callback_data="ct " + str(city_list[i][2]))
        markup.add(city_btn)
    await bot.send_message(message.from_user.id,
                           constants.choose_right_city,
                           reply_markup=markup)


async def city_call_change(callback: types.CallbackQuery, state=FSMContext):
    lst = callback.data.split(' ')
    city = cities[int(lst[1])]
    await users_db.create_or_update_user(callback.from_user.id, city)
    await callback.answer(links.success_city)
    await state.finish()
    await russian.menu(callback.from_user.id)


async def skip_call(callback: types.CallbackQuery):
    await callback.answer()


async def choose_language(message: types.Message):
    if users_db.have_user(message.from_user.id):
        await russian.menu(message.from_user.id)
    else:
        await bot.send_message(message.from_user.id,
                               text=links.welcome_text,
                               parse_mode='Markdown')
        await city_start(message)


async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        links.help_text,
        parse_mode='Markdown'
    )


async def message_filter(message: types.Message):
    await bot.send_message(message.from_user.id, constants.wrong_name)


def check_text(dp: Dispatcher):
    dp.register_message_handler(choose_language, commands=['start'])
    dp.register_message_handler(city_start, text=links.menu_change_city)
    dp.register_message_handler(city_name, state=CityOfUser.city)
    dp.register_callback_query_handler(skip_call, Text(equals='skip_call'))
    dp.register_callback_query_handler(
        city_call_change,
        Text(startswith='ct'),
        state=CityOfUser.city)
    dp.register_message_handler(help_command, commands=["help"])
    dp.register_message_handler(message_filter)
