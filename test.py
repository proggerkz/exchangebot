from database import ad_collection
import database
# database.change_moderator_ad_to_real(12)

collection = ad_collection.find({
    "city": "АЛМАТЫ"
})
for col in collection:
    print(col)
    col["city"] = "АЛМАТЫ(АЛМАТЫ)"
    col["user_city"] = None
    ad_collection.update_one({"_id": col["_id"]},
                             {"$set": col},
                             upsert=False
    )
