from aiogram import Dispatcher, types
from create_bot import dp, bot
from links import rus_country, countryCities
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.rus_menu_kb import rus_menu_kb_button
from keyboards.countries import rus_countries


async def rus_lang(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Выберите вид услуги пожалуйста', reply_markup=rus_menu_kb_button)
    await callback.answer()


async def print_countries(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите в какой стране вы живете', reply_markup=rus_countries)


async def print_cities_in_country(message: types.Message):
    i = 0
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    countries = countryCities.get(message.text)
    while i < len(countries):
        if i + 1 == len(countries):
            b = KeyboardButton(countries[i])
            markup.add(b)
            i += 1
        else:
            b1 = KeyboardButton(countries[i])
            b2 = KeyboardButton(countries[i + 1])
            markup.add(b1, b2)
            i += 2
    await bot.send_message(message.from_user.id, 'Выберите в каком городе вы живете', reply_markup=markup)


def register_step_russian(dp : Dispatcher):
    dp.register_callback_query_handler(rus_lang, text="rus_lang")
    dp.register_message_handler(print_countries, text='Обмен игрушками')
    for i in range(len(rus_country)):
        dp.register_message_handler(print_cities_in_country, text=rus_country[i])
