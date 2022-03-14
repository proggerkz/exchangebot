from database import ad_collection
import database
# database.change_moderator_ad_to_real(12)

# collection = ad_collection.find({
#     "city": "АЛМАТЫ"
# })
# for col in collection:
#     print(col)
#     col["city"] = "АЛМАТЫ(АЛМАТЫ)"
#     col["user_city"] = None
#     ad_collection.update_one({"_id": col["_id"]},
#                              {"$set": col},
#                              upsert=False
#     )

# from db import liked_ads
#
#
# def add_connection(user_from_id, user_to_id, ad_from_id, ad_to_id, username):
#     liked_ads.create_data(user_from_id, user_to_id, ad_from_id, ad_to_id, username)
#
#
# add_connection(609616860, 405696444, 49, 51, "dias0x1B")