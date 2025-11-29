from middleware.authentication import create_token
from login.generate_otp import generate_otp_record, validate_otp_record
from login.user_create_find import find_or_create_user
from utils.helpers import serialize_user
from database.database import users_collection
from bson import ObjectId
from datetime import datetime


# ------------------------------------------------------------
# 0. SUPPORT USER QUICK LOGIN (always accepted)
# ------------------------------------------------------------
async def support_user_login(key: str, otp: str):
    if key == "support@skillobal.com" and otp == "123123":
        existing_user = await users_collection.find_one({"email": key})

        if not existing_user:
            support_user = {
                "name": "Support User",
                "email": key,
                "mobile": 9999999999,
                "profile_image": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                "selected_categories": [],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            await users_collection.insert_one(support_user)
            existing_user = await users_collection.find_one({"email": key})

        serialized = await serialize_user(existing_user)
        token = create_token(serialized["id"])

        return {
            "success": True,
            "purpose": "login",
            "user": serialized,
            "token": token
        }

    return None  # not support login


# ------------------------------------------------------------
# 1. LOGIN OTP (normal users)
# ------------------------------------------------------------
async def verify_login_otp(key: str, otp: str):
    record, error = await validate_otp_record(key, otp)
    if error:
        return {"success": False, "message": error}

    user = await find_or_create_user(key)
    serialized = await serialize_user(user)
    token = create_token(serialized["id"])

    return {
        "success": True,
        "purpose": "login",
        "user": serialized,
        "token": token
    }


# ------------------------------------------------------------
# 2. SECONDARY OTP (verify email/mobile when logged in)
# ------------------------------------------------------------
async def verify_secondary_otp(user_id: str, key: str, otp: str):
    record, error = await validate_otp_record(key, otp)
    if error:
        return {"success": False, "message": error}

    update_doc = {}

    if "@" in key:
        update_doc = {"email": key, "email_verified": True}
    else:
        update_doc = {"mobile": int(key), "mobile_verified": True}

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_doc}
    )

    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    serialized = await serialize_user(updated_user)

    return {
        "success": True,
        "purpose": "secondary_verification",
        "message": "Contact verified successfully",
        "user": serialized
    }


# ------------------------------------------------------------
# 3. MAIN VERIFY OTP (used by route)
# ------------------------------------------------------------
async def verify_otp(key: str, otp: str, current_user):

    # ⭐ check support user first
    support_login = await support_user_login(key, otp)
    if support_login:
        return support_login

    # ⭐ Login flow when user NOT logged in
    if current_user is None:
        return await verify_login_otp(key, otp)

    # ⭐ Secondary verification when user IS logged in
    user_id = current_user.get("user_id")  # your token payload uses "user_id"
    if not user_id:
        return {"success": False, "message": "Invalid authentication token"}

    return await verify_secondary_otp(user_id, key, otp)


# ------------------------------------------------------------
# (Utility) Generate OTP
# ------------------------------------------------------------
async def generate_otp(key: str):
    otp = await generate_otp_record(key)
    return otp