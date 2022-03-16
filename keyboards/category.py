from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from russian.constants import cancel_text, menu_text
from russian.categories import categories

category_key_list = list(categories.keys())


def create_category_btn(category_btn_id, category_list):
    i = 0
    while i < len(category_list):
        if i + 1 == len(category_list):
            b = KeyboardButton(category_list[i])
            category_btn_id.add(b)
            i += 1
        else:
            b1 = KeyboardButton(category_list[i])
            b2 = KeyboardButton(category_list[i + 1])
            category_btn_id.add(b1, b2)
            i += 2


category_with_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True)
create_category_btn(category_with_menu_btn, category_key_list)
category_with_menu_btn.insert(menu_text)
category_btn_with_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
create_category_btn(category_btn_with_cancel, category_key_list)
category_btn_with_cancel.insert(cancel_text)