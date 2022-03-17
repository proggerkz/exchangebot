from database import ad_db

search_col = ad_db["search"]

# Create search data


def create_search_data(user_id, search_text):
    search = list(search_col.find())
    _id = -1
    if len(search) == 0:
        _id = 1
    else:
        _id = int(search[-1].get("_id")) + 1
    _id = str(_id)
    search_col.insert_one({
        "user_id": user_id,
        "_id": _id,
        "text": search_text,
        "cnt": 0
    })
    return _id


# Get search by idd
def get_search_id(_id):
    search = search_col.find_one({
        "_id": _id
    })
    return search


# Set cnt
def set_cnt(_id):
    search = search_col.find_one({
        "_id": _id
    })
    search["cnt"] += 1
    search_col.update_one(
        {
            "_id": _id,
        },
        {
            "$set": search,
        },
        upsert=False
    )
    return search["cnt"]


# Get search text
def get_search_text(_id):
    search = search_col.find_one({
        "_id": _id
    })
    return search.get("text")