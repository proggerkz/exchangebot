from config import db_data
from pymongo import MongoClient

cluster = MongoClient(db_data)
user_db = cluster["users"]
user_col = user_db["user_list"]


# Проверка если существует участник по нику
def have_user(username):
    obj = user_col.find_one({"username": username})
    if obj is None:
        return False
    else:
        post = user_col.find_one({"username": username})
        post["active"] = True
        user_col.update_one({"username": username}, {"$set": post}, upsert=False)
        return True


# Создание или обновление города проживания участника
async def create_or_update_user(username, user_city):
    obj = user_col.find_one({"username": username})
    if obj is None:
        new_user = {
            "username": username,
            "user_city": user_city,
            "active": True
        }
        user_col.insert_one(new_user)
    else:
        obj["active"] = True
        obj["user_city"] = user_city
        user_col.update_one({"username": username}, {"$set": obj}, upsert=False)