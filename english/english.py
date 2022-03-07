from aiogram import Dispatcher, types
from create_bot import dp
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton


async def eng_lang(callback: types.CallbackQuery):
    await callback.answer('In development')


def register_step_russian(dp : Dispatcher):
    dp.register_callback_query_handler(eng_lang, text="rus_lang")
