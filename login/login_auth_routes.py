from fastapi import APIRouter, HTTPException
from login.email_sender import send_email
from login.generate_otp import generate_otp, verify_otp
from login.mobile_sms_sender import send_sms_otp  # import your SMS function  
from models.schemas import OTPRequest, VerifyRequest
from middleware.authentication import create_token
from database.database import users_collection

router = APIRouter(tags=["Auth"])

@router.post("/send-otp")
async def send_otp(request: OTPRequest):  # EmailRequest has "key" field (email or mobile)
    otp = await generate_otp(request.login_key)

    # If the key contains '@', treat as email, else treat as mobile
    if "@" in request.login_key:
        success = send_email(request.login_key, otp)
    else:
        success = await send_sms_otp(request.login_key, otp)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

    return {"message": "OTP sent successfully", "login_key": request.login_key}


@router.post("/verify-otp")
async def verify_otp_route(request: VerifyRequest):
    verified = await verify_otp(request.login_key, request.otp)

    if not verified:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # ✅ Create token
    token = create_token(request.login_key)

    # ✅ Define user details based on login type
    if "@" in request.login_key:  # Email login
        user_data = {
            "email": request.login_key,
            "mobile": "0000000000",
            "profile_image": "https://cdn-icons-png.flaticon.com/512/149/149071.png"
        }
    else:  # Mobile login
        user_data = {
            "mobile": request.login_key,
            "email": "example@gmail.com",
            "profile_image": "https://cdn-icons-png.flaticon.com/512/149/149071.png"
        }

    # ✅ Upsert user record in MongoDB
    await users_collection.update_one(
        {"$or": [{"email": user_data.get("email")}, {"mobile": user_data.get("mobile")}]},
        {"$set": user_data},
        upsert=True
    )

    # ✅ Response
    return {
        "message": "Login successful",
        "user": user_data,
        "token": token
    }

