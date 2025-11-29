from fastapi import APIRouter, Depends
from login.email_sender import send_email
from login.mobile_sms_sender import send_sms_otp
from models.schemas import OTPRequest, VerifyRequest
from middleware.exceptions import CustomError
from middleware.authentication import optional_auth
from login.otp_controller import generate_otp, verify_otp

router = APIRouter(tags=["Auth"])


@router.post("/send-otp")
async def send_otp_route(request: OTPRequest):
    otp = await generate_otp(request.login_key)

    if "@" in request.login_key:
        success = send_email(request.login_key, otp)
    else:
        success = await send_sms_otp(request.login_key, otp)

    if not success:
        raise CustomError("Failed to send OTP", 500)

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp")
async def verify_otp_route(request: VerifyRequest, current_user=Depends(optional_auth)):

    result = await verify_otp(request.login_key, request.otp, current_user)

    if not result["success"]:
        raise CustomError(result["message"], 400)

    # LOGIN RESPONSE
    if result["purpose"] == "login":
        return {
            "message": "Login successful",
            "user": result["user"],
            "token": result["token"]
        }

    # SECONDARY VERIFY RESPONSE
    return {
        "message": result["message"],
        "user": result["user"]
    }