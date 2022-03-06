from aiogram import types
from aiogram.dispatcher import FSMContext
import links
import database
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()


async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply(links.create_add_text)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь введите название игрушки')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь опишите свои игрушку и свои предпочтения')


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data['username'] = message.from_user.username
    await database.ad_add_moderator(state)
    await state.finish()
