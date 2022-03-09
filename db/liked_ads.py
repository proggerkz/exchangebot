from database import ad_db
import database
liked_ads = ad_db['liked_ads']


# Уже имеется лайк
def have_connection(user_from_id, user_to_id, ad_from_id, ad_to_id):
    if liked_ads.find_one({
        "user_from_id": user_from_id,
        "user_to_id": user_to_id,
        "ad_from_id": ad_from_id,
        "ad_to_id": ad_to_id,
    }) is not None:
        return True
    else:
        return False


# Добавление в liked ads данные
def create_data(user_from_id, user_to_id, ad_from_id, ad_to_id, username):
    data = {
        "user_from_id": user_from_id,
        "user_to_id": user_to_id,
        "ad_from_id": ad_from_id,
        "ad_to_id": ad_to_id,
        "username": username,
    }
    liked_ads.insert_one(data)


# Получение обьявлении которым понравилась моя обьявление
def get_my_ad(user_to_id):
    while True:
        ad = liked_ads.find_one({
            "user_to_id": user_to_id
        })
        if ad is None:
            return None
        else:
            ad_from_id = ad.get("ad_from_id")
            ad_to_id = ad.get("ad_to_id")
            ad_from = database.get_ad_by_ad_id(ad_from_id)
            ad_to = database.get_ad_by_ad_id(ad_to_id)
            if ad_from is None or ad_to is None:
                liked_ads.delete_one(ad)
            else:
                return ad


# Удаление соединения из БД
def delete_connection(user_from_id, user_to_id, ad_from_id, ad_to_id):
    liked_ads.delete_one({
        "user_from_id": user_from_id,
        "user_to_id": user_to_id,
        "ad_from_id": ad_from_id,
        "ad_to_id": ad_to_id
    })

