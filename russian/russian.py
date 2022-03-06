from aiogram import Dispatcher, types
from create_bot import dp, bot
from links import rus_country, countryCities
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.rus_menu_kb import rus_menu_kb_button
from keyboards.countries import rus_countries
from russian import work_with_add
from russian.work_with_add import FSMAdmin
from db import users_db
# Need to add database if they import their data


async def menu(user_id):
    await bot.send_message(user_id, 'Выберите вид услуги пожалуйста', reply_markup=rus_menu_kb_button)


async def rus_lang(callback: types.CallbackQuery):
    if users_db.have_user(callback.from_user.username):
        await menu(callback.from_user.id)
    else:
        await bot.send_message(callback.from_user.id, 'Напишите пожалуйста на кириллице в каком городе вы проживаете')
    await callback.answer()


async def print_adds_in_cities(message: types.Message):
    await users_db.create_or_update_user(message.from_user.username, message.text)


def register_step_russian(dp : Dispatcher):
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
