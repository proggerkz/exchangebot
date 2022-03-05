from aiogram import types
from create_bot import dp, bot
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from english import english
from russian import russian


def on_startup(_):
    print('Bot is online now')


@dp.message_handler(commands=['start'])
async def choose_language(message: types.message):
    markup = InlineKeyboardMarkup(row_width=2)
    rus = InlineKeyboardButton(text='Русский', callback_data="rus_lang")
    eng = InlineKeyboardButton(text='English', callback_data="eng_lang")
    markup.add(rus, eng)
    await bot.send_message(message.from_user.id,
                           text="Welcome to the our telegram bot, choose the language to start using the bot",
                           reply_markup=markup)


russian.register_step_russian(dp)
english.register_step_russian(dp)
executor.start_polling(dp, skip_updates=True)
