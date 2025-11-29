from datetime import datetime
from database.database import users_collection
from utils.helpers import serialize_user

DEFAULT_PROFILE = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

async def find_or_create_user(key: str):
    # Prepare lookup
    if "@" in key:
        lookup = {"email": key}
        default_email = key
        default_mobile = 0
    else:
        lookup = {"mobile": int(key)}
        default_mobile = int(key)
        default_email = ""

    existing = await users_collection.find_one(lookup)

    if existing:
        await users_collection.update_one(
            lookup,
            {"$set": {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
        )
        return await users_collection.find_one(lookup)

    # New user
    default_data = {
        "name": "User",
        "profile_image": DEFAULT_PROFILE,
        "selected_categories": [],
        "email": default_email,
        "mobile": default_mobile,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    result = await users_collection.insert_one(default_data)
    return await users_collection.find_one({"_id": result.inserted_id})