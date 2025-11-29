import random
from datetime import datetime, timedelta
from database.database import db

OTP_EXPIRY_MINUTES = 5

DEFAULT_EMAIL = "support@skillobal.com"
DEFAULT_OTP = "123123"


# ------------------------------------------------------------
# GENERATE OTP
# ------------------------------------------------------------
async def generate_otp_record(key: str):

    # ⭐ 1. Special default support OTP
    if key == DEFAULT_EMAIL:
        return DEFAULT_OTP

    # ⭐ 2. Normal OTP Flow
    otp = str(random.randint(100000, 999999))

    collection = db.email_otps if "@" in key else db.mobile_otps
    field = "email" if "@" in key else "mobile"

    await collection.update_one(
        {field: key},
        {
            "$set": {
                "otp": otp,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "used": False
            }
        },
        upsert=True
    )

    return otp


# ------------------------------------------------------------
# VALIDATE OTP
# ------------------------------------------------------------
async def validate_otp_record(key: str, otp: str):

    # ⭐ 1. Special support login bypass
    if key == DEFAULT_EMAIL and otp == DEFAULT_OTP:
        return {"otp": DEFAULT_OTP}, None   # No DB check required

    # ⭐ 2. Normal OTP Validation
    collection = db.email_otps if "@" in key else db.mobile_otps
    field = "email" if "@" in key else "mobile"

    record = await collection.find_one({field: key})
    if not record:
        return None, "OTP not found"

    created = datetime.strptime(record["created_at"], "%Y-%m-%d %H:%M:%S")
    expired = datetime.now() > created + timedelta(minutes=OTP_EXPIRY_MINUTES)

    if expired or record.get("used") or record["otp"] != otp:
        return None, "Invalid or expired OTP"

    await collection.update_one({field: key}, {"$set": {"used": True}})
    return record, None