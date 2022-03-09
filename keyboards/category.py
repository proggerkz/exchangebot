from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from links import category
from russian.constants import cancel_text


def create_category_btn(category_btn):
    i = 0
    while i < len(category):
        if i + 1 == len(category):
            b = KeyboardButton(category[i])
            category_btn.add(b)
            i += 1
        else:
            b1 = KeyboardButton(category[i])
            b2 = KeyboardButton(category[i + 1])
            category_btn.add(b1, b2)
            i += 2


category_btn = ReplyKeyboardMarkup(resize_keyboard=True)
create_category_btn(category_btn)
category_with_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True)
create_category_btn(category_with_menu_btn)
category_with_menu_btn.add('Меню')
category_btn_with_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
create_category_btn(category_btn_with_cancel)
category_btn_with_cancel.add(cancel_text)