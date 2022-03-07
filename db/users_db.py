from config import db_data
from pymongo import MongoClient
import database

cluster = MongoClient(db_data)
user_db = cluster["users"]
user_col = user_db["user_list"]


# Проверка если существует участник по нику
def have_user(user_id):
    obj = user_col.find_one({"user_id": user_id})
    if obj is None:
        return False
    else:
        post = user_col.find_one({"user_id": user_id})
        post["active"] = True
        user_col.update_one({"user_id": user_id}, {"$set": post}, upsert=False)
        return True


# Создание или обновление города проживания участника
async def create_or_update_user(user_id, user_city):
    obj = user_col.find_one({"user_id": user_id})
    if obj is None:
        new_user = {
            "user_id": user_id,
            "user_city": user_city,
            "user_city_id": 0,
            "active": True,
            "user_lang": 'rus'
        }
        user_col.insert_one(new_user)
    else:
        obj["active"] = True
        obj["user_city"] = user_city
        obj["user_city_id"] = 0
        user_col.update_one({"user_id": user_id}, {"$set": obj}, upsert=False)


# Геттер для города
def get_city_of_user(user_id):
    obj = user_col.find_one({"user_id": user_id})
    return obj.get("user_city")


# Получиение по юзернейму следующего обьявления для определенного участника
def get_next(user_id):
    obj = user_col.find_one({"user_id": user_id})
    obj["user_city_id"] += 1
    user_col.update_one({"user_id": user_id}, {"$set": obj}, upsert=False)
    ad = database.get_ad_by_city_id(obj["user_city"], obj["user_city_id"])
    return ad


# Сделать участника пассивным
def make_passive(user_id):
    obj = user_col.find_one({"user_id": user_id})
    obj["active"] = False
    user_col.update_one({"user_id": user_id}, {"$set": obj}, upsert=False)

