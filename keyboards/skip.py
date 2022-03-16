from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from russian import constants

b1 = KeyboardButton(constants.skip_text)
b2 = KeyboardButton(constants.cancel_text)
skip_btn = ReplyKeyboardMarkup(resize_keyboard=True)
skip_btn.add(b1, b2)