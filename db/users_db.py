import database
from database import cluster

user_db = cluster["users"]
user_col = user_db["user_list"]


def change_rating(user_id, rating):
    obj = user_col.find_one({
        "user_id": user_id
    })

    obj["rating"]["cnt"] += 1
    obj["rating"]["amount"] += rating
    user_col.update_one(
        {"user_id": user_id},
        {"$set": obj},
        upsert=False
    )


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
    user_city = user_city.upper()
    obj = user_col.find_one({"user_id": user_id})
    if obj is None:
        new_user = {
            "user_id": user_id,
            "user_city": user_city,
            "user_city_id": 0,
            "active": True,
            "user_lang": 'rus',
            "is_premium": False,
            "rating": {
                "cnt": 0,
                "amount": 0
            },
            "last_category": {
                "name": "Nothing",
                "id": 0,
            },
            "search_list": [],
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
def get_next(user_id, category_id):
    obj = user_col.find_one({"user_id": user_id})
    obj["user_city_id"] += 1
    user_col.update_one({"user_id": user_id}, {"$set": obj}, upsert=False)
    ad = database.get_ad_by_city_id(obj["user_city"], obj["user_city_id"], category_id)
    return ad


# Сделать участника пассивным
def make_passive(user_id):
    obj = user_col.find_one({"user_id": user_id})
    obj["active"] = False
    user_col.update_one({"user_id": user_id}, {"$set": obj}, upsert=False)


# Количество активных юзеров
def active_users():
    obj = user_col.find({"active": True})
    return len(list(obj))


# Получить реитинг участника
def get_rating(user_id):
    obj = user_col.find_one({
        "user_id": user_id
    })
    rate_cnt = obj.get("rating", {}).get("cnt")
    rate_amount = obj.get("rating", {}).get("amount")
    if rate_cnt == 0:
        return 0
    else:
        return rate_amount / rate_cnt


# Получить последнюю категорию
def last_category(user_id):
    obj = user_col.find_one({
        "user_id": user_id
    })
    category_name = obj.get("last_category", {}).get("name")
    category_id = obj.get("last_category", {}).get("id")
    return [category_name, category_id]


# Получить последнее обьявление
def get_last(user_id, category_id):
    obj = user_col.find_one({
        "user_id": user_id
    })
    user_city = obj['user_city']
    return database.get_last(category_id, user_city)


# Поменять категорию последнюю
def change_category(user_id, category_name, category_id):
    obj = user_col.find_one({
        "user_id": user_id
    })
    obj["last_category"]["name"] = category_name
    obj["last_category"]["id"] = category_id
    user_col.update_one(
        {"user_id": user_id},
        {"$set": obj},
        upsert=False
    )


# Все активные юзера
def users_all():
    obj = user_col.find({"active": True})
    return list(obj)


def get_is_premium(user_id):
    obj = user_col.find_one({
        "user_id": user_id
    })
    return obj.get('is_premium')


# Update search
def upd_user(user_id, search_txt):
    obj = user_col.find_one({
        "user_id": user_id
    })
    arr = list(obj.get("search_list"))
    if search_txt in arr:
        arr.remove(search_txt)
    if len(arr) == 10:
        arr.pop()
    arr.append(search_txt)
    obj["search_list"] = arr
    user_col.update_one(
        {
            "user_id": user_id,
        },
        {
            "$set": obj
        },
        upsert=False
    )


# Get search list
def get_search_list(user_id):
    obj = user_col.find_one(
        {
            "user_id": user_id
        }
    )
    return list(obj.get("search_list"))
