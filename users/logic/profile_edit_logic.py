from database.database import users_collection
from bson import ObjectId
from middleware.exceptions import CustomError   # ✅
from datetime import datetime

async def update_user_profile(user_id: str, update_data: dict):

    try:
        oid = ObjectId(user_id)
    except:
        raise CustomError("Invalid user ID", 400)

    if not update_data:
        raise CustomError("No fields to update", 400)

    if "selected_categories" in update_data:
        object_ids = []
        for cid in update_data["selected_categories"]:
            try:
                object_ids.append(ObjectId(cid))
            except:
                raise CustomError(f"Invalid category ID: {cid}", 400)

        update_data["selected_categories"] = object_ids

    restricted = ["_id", "password", "user_id", "email"]
    for field in restricted:
        update_data.pop(field, None)

    update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = await users_collection.update_one(
        {"_id": oid},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise CustomError("User not found", 404)

    return {"message": "Profile updated successfully"}
