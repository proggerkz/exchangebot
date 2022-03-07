from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Обмен игрушками')
b2 = KeyboardButton('Создать обьявление')
b3 = KeyboardButton('Мои обьявления')
b4 = KeyboardButton('Поменять город проживания')
rus_menu_kb_button = ReplyKeyboardMarkup(resize_keyboard=True)
rus_menu_kb_button.add(b1, b2)
rus_menu_kb_button.add(b3, b4)