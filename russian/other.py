from aiogram import Dispatcher, types
from create_bot import dp, bot
from russian import constants


async def message_filter(message: types.Message):
    await bot.send_message(message.from_user.id, constants.wrong_name)


def check_text(dp: Dispatcher):
    dp.register_message_handler(message_filter)
