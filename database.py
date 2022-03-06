import config
from pymongo import MongoClient
# import gridfs

db_data = "mongodb+srv://" + config.DB_USERNAME + ":" + config.DB_PASSWORD + "@cluster0.zcoz3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(db_data)
ad_db = cluster["ads"]
ad_collection = ad_db["ads"]
moderator_ads = ad_db["moderator_ads"]
# fs = gridfs[ad_db]


# Все обьявления определенного города
def get_ad(city_name):
    ads = ad_collection.find({"city": city_name})
    return ads


# Одобрение модератором обьявление вывести на общую
def change_moderator_ad_to_real(_id):
    cur_ad = moderator_ads.find_one({"_id": str(_id)})
    if cur_ad is not None:
        moderator_ads.delete_one({"_id": str(_id)})
        ad_collection.insert_one(cur_ad)


# Удаление обьявления с основной
def delete_ad(_id):
    ad_collection.delete_one({"_id": _id})


def get_max_id_in_collection(collection):
    res = 0
    for col in collection:
        res = max(res, int(col["_id"]))
    return res


# Добавить обьявление на модераторскую
async def ad_add_moderator(state):
    async with state.proxy() as data:
        d = dict(data)
        m_list = moderator_ads.find()
        ad_list = ad_collection.find()
        m = max(get_max_id_in_collection(m_list), get_max_id_in_collection(ad_list))
        m += 1
        d["_id"] = str(m)
        moderator_ads.insert_one(d)


# Удаление обьявления с модераторской
def delete_add_moderator(_id):
    moderator_ads.delete_one({"_id": str(_id)})


# Обьявление определенного участника
def get_user_ads(username):
    ads = ad_collection.find({"username": username})
    return ads
