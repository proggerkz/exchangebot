from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import links
i = 0
rus_countries = ReplyKeyboardMarkup(resize_keyboard=True)
while i < len(links.rus_country):
    if i + 1 == len(links.rus_country):
        b = KeyboardButton(links.rus_country[i])
        rus_countries.add(b)
        i += 1
    else:
        b1 = KeyboardButton(links.rus_country[i])
        b2 = KeyboardButton(links.rus_country[i + 1])
        rus_countries.add(b1, b2)
        i += 2
