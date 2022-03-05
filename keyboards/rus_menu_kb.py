from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Обмен игрушками')
b2 = KeyboardButton('Создать обьявление')

rus_menu_kb_button = ReplyKeyboardMarkup(resize_keyboard=True)
rus_menu_kb_button.add(b1, b2)