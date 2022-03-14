from db.users_db import user_db
from db import users_db
rated = user_db["rated"]


def have_connection(user_from, user_to):
    obj = rated.find_one(
        {
            "user_from": user_from,
            "user_to": user_to
        }
    )
    return obj


def change_rating(user_from, user_to, rating):
    rated.insert_one({
        "user_from": user_from,
        "user_to": user_to
    })
    users_db.change_rating(user_to, rating)
