from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Казахстан')
b2 = KeyboardButton('Россия')
b3 = KeyboardButton('Белоруссия')
b4 = KeyboardButton('Украина')

rus_countries = ReplyKeyboardMarkup()
rus_countries.add(b1, b2)
rus_countries.add(b3, b4)