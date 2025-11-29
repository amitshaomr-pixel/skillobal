from bson import ObjectId
from database.database import users_collection, categories_collection
from middleware.exceptions import CustomError

async def save_interest_categories(user_id: str, category_ids: list):

    # Convert user_id to ObjectId
    try:
        user_oid = ObjectId(user_id)
    except:
        raise CustomError("Invalid user ID from token")

    # Validate and convert category IDs
    valid_oids = []
    for cid in category_ids:
        try:
            oid = ObjectId(cid)
            valid_oids.append(oid)
        except:
            raise CustomError(f"Invalid category ID: {cid}")

    # Fetch valid categories (id + name)
    categories = await categories_collection.find(
        {"_id": {"$in": valid_oids}},
        {"name": 1}
    ).to_list(None)

    if len(categories) != len(valid_oids):
        raise CustomError("One or more categories do not exist")

    # Store only category ObjectIds
    await users_collection.update_one(
        {"_id": user_oid},
        {"$set": {"selected_categories": valid_oids}}
    )

    # Prepare response: id + name
    result = [
        {
            "id": str(cat["_id"]),
            "name": cat.get("name", "")
        }
        for cat in categories
    ]

    return result