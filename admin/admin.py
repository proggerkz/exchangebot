from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import database
from db import users_db
from admin import constants


async def moderator(message: types.Message):
    if message.from_user.username in config.moderators_username:
        moderator_ad = database.get_moderator_ad()
        if moderator_ad is None:
            await bot.send_message(message.from_user.id, 'No adds')
        else:
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text=constants.approve, callback_data='mod_ok ' + moderator_ad["_id"])
            b2 = InlineKeyboardButton(text=constants.delete, callback_data='mod_del ' + moderator_ad["_id"])
            markup.add(b1, b2)
            await bot.send_photo(message.from_user.id,
                                 moderator_ad.get('photo'),
                                 f'{moderator_ad.get("name")}\nОписание: {moderator_ad.get("description")}',
                                 reply_markup=markup)


async def delete_moderator(callback: types.CallbackQuery):
    if callback.from_user.username in config.moderators_username:
        _id = callback.data.split(' ')[1]
        if database.moderator_ads.find_one({"_id": _id}):
            database.moderator_ads.delete_one({"_id": _id})
            await callback.answer(constants.add_deleted)
            await moderator(callback)
        else:
            await callback.answer(constants.already_done)
    else:
        await callback.answer(constants.not_moderator)


async def stats(message: types.Message):
    if message.from_user.username in config.moderators_username:
       await bot.send_message(message.from_user.id, constants.users_text +
                              str(users_db.active_users()))


async def approve_moderator(callback: types.CallbackQuery):
    if callback.from_user.username in config.moderators_username:
        _id = callback.data.split(' ')[1]
        if database.moderator_ads.find_one({"_id": _id}):
            database.change_moderator_ad_to_real(_id)
            await callback.answer(constants.add_approved)
            await moderator(callback)
        else:
            await callback.answer(constants.already_done)
    else:
        await callback.answer(constants.not_moderator)


def register_step_admin(dp: Dispatcher):
    dp.register_message_handler(moderator, commands=['moderator', 'admin'])
    dp.register_message_handler(stats, commands=['stats'])
    dp.register_callback_query_handler(delete_moderator, Text(startswith='mod_del'))
    dp.register_callback_query_handler(approve_moderator, Text(startswith='mod_ok'))
