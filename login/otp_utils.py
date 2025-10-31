# otp_utils.py

import random
from datetime import datetime, timedelta
from core.database import db

OTP_EXPIRY_MINUTES = 5

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Generate OTP and store
async def generate_otp(key: str) -> str:
    """
    key can be email or mobile
    """
    otp = str(random.randint(100000, 999999))

    # Choose collection based on key type
    if "@" in key:
        collection = db.email_otps
        field = "email"
    else:
        collection = db.mobile_otps
        field = "mobile"

    await collection.update_one(
        {field: key},
        {"$set": {"otp": otp, "created_at": now_str(), "used": False}},
        upsert=True
    )
    return otp


# Verify OTP
async def verify_otp(key: str, user_otp: str) -> bool:
    if "@" in key:
        collection = db.email_otps
        field = "email"
    else:
        collection = db.mobile_otps
        field = "mobile"

    record = await collection.find_one({field: key})
    if not record:
        return False

    expired = datetime.now() > datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=OTP_EXPIRY_MINUTES)
    if expired or record.get("used") or record["otp"] != user_otp:
        return False

    # Mark OTP as used
    await collection.update_one({field: key}, {"$set": {"used": True}})

    # Upsert user document in users collection
    await db.users.update_one(
        {field: key},
        {"$set": {"updated_at": now_str()}, "$setOnInsert": {field: key, "created_at": now_str()}},
        upsert=True
    )
    return True
