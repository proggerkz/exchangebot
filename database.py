from config import db_data
from pymongo import MongoClient
# import gridfs


cluster = MongoClient(db_data)
ad_db = cluster["ads"]
ad_collection = ad_db["ads"]
max_id = ad_db["max_id"]
moderator_ads = ad_db["moderator_ads"]


# Одобрение модератором обьявление вывести на общую
def change_moderator_ad_to_real(_id):
    cur_ad = moderator_ads.find_one({"_id": str(_id)})
    if cur_ad is not None:
        moderator_ads.delete_one({"_id": str(_id)})
        ad_collection.insert_one(cur_ad)


# Получить максимальный ид из всех участников
def get_max_id_in_collection(collection):
    res = 0
    for col in collection:
        res = max(res, int(col["_id"]))
    return res


# Добавить обьявление на модераторскую
async def ad_add_moderator(state):
    async with state.proxy() as data:
        d = dict(data)
        m = get_max_id_in_collection(max_id.find()) + 1
        d["_id"] = str(m)
        moderator_ads.insert_one(d)
        max_id.insert_one({"_id": str(m)})


# Удаление обьявления с основной
def delete_add_ads(_id):
    ad_collection.delete_one({"_id": str(_id)})


# Обьявление определенного участника
def get_user_ads(user_id):
    ads = list(ad_collection.find({"user_id": user_id}))
    return ads


# Получение обьявления по индексу по городам
def get_ad_by_city_id(city, city_id, category):
    cur_db = list(ad_collection.find({"city": city, "category": category}))
    if len(cur_db) == 0:
        return None
    else:
        city_id = city_id % len(cur_db)
        return cur_db[city_id]


# Получение обьявление по ид обьявления
def get_ad_by_ad_id(ad_id):
    cur_db = ad_collection.find_one({"_id": str(ad_id)})
    return cur_db


# Получение обьявление из модераторов
def get_moderator_ad():
    ad = moderator_ads.find_one()
    return ad


