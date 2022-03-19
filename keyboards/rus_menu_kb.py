from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import links
b1 = KeyboardButton(links.menu_search)
b3 = KeyboardButton(links.menu_exchange)
b2 = KeyboardButton(links.menu_create)
b4 = KeyboardButton(links.menu_my_ads)
b5 = KeyboardButton(links.menu_change_city)
b6 = KeyboardButton(links.menu_profile)
b7 = KeyboardButton(links.menu_statistics)

rus_menu_kb_button = ReplyKeyboardMarkup(resize_keyboard=True)
rus_menu_kb_button.add(b1, b2)
rus_menu_kb_button.add(b3, b4)
rus_menu_kb_button.add(b5, b6)
rus_menu_kb_button.add(b7)