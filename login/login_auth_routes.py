from fastapi import APIRouter, HTTPException
from login.email_sender import send_email
from login.otp_utils import generate_otp, verify_otp
from login.mobile_sms_sender import send_sms_otp  # import your SMS function  
from models.schemas import OTPRequest, VerifyRequest
from core.authentication import create_token

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
    if verified:
        token = create_token(request.login_key)
        return {
            "message": "OTP verified successfully",
            "login_key": request.login_key,
            "token": token
        }
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

