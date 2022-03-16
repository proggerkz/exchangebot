from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from russian.constants import exchange_text, cell_text, cancel_text

type_btn = ReplyKeyboardMarkup(resize_keyboard=True)
exchange_button = KeyboardButton(exchange_text)
cell_button = KeyboardButton(cell_text)
cancel_button = KeyboardButton(cancel_text)
type_btn.add(exchange_button, cell_button)
type_btn.add(cancel_button)
