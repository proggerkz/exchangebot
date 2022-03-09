from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from russian.constants import cancel_text

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(cancel_text)
cancel_kb.add(button)
