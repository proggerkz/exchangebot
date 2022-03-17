from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from russian.constants import cancel_text, free_text, equalize_text
cost_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(free_text)
b2 = KeyboardButton(equalize_text)
b3 = KeyboardButton(cancel_text)
cost_kb.add(b1, b2)
cost_kb.add(b3)