from aiogram import Dispatcher, types
from create_bot import dp, bot


async def message_filter(message: types.Message):
    await bot.send_message(message.from_user.id, 'Кажется вы неправильно написали название города или пока что вашего города не существует'
                           'в списке городов')

def check_text(dp : Dispatcher):
    dp.register_message_handler(message_filter)
