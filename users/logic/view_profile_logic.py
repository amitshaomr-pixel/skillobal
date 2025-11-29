from database.database import users_collection
from bson import ObjectId
from middleware.exceptions import CustomError   # ✅

async def get_user_profile(user_id: str):

    try:
        oid = ObjectId(user_id)
    except:
        raise CustomError("Invalid user ID", 400)

    user = await users_collection.find_one({"_id": oid})

    if not user:
        raise CustomError("User not found", 404)

    user["_id"] = str(user["_id"])

    return {
        "id": user["_id"],
        "name": user.get("name"),
        "email": user.get("email"),
        "mobile": user.get("mobile"),
        "selected_categories": [str(cid) for cid in user.get("selected_categories", [])],
        "profile_image": user.get("profile_image"),
    }
