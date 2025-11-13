#mobile_sms_sender.py

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

COMBIRDS_API_URL = "https://smsapi.edumarcsms.com/api/v1/sendsms"
COMBIRDS_API_KEY = os.getenv("COMBIRDS_API_KEY") 
SENDER_ID = os.getenv("COMBIRDS_SENDER_ID")
TEMPLATE_ID = os.getenv("COMBIRDS_TEMPLATE_ID")


async def send_sms_otp(mobile: str, otp: str):
    """
    Send OTP SMS exactly matching the DLT template.
    `user_name` replaces the first {#var#}, otp replaces the second {#var#}.
    """
    
    message = f"Your OTP for verification is: {otp}. OTP is confidential, refrain from sharing it with anyone. By Edumarc Technologies"

    payload = {
        "message": message,
        "senderId": SENDER_ID,
        "number": [f"91{mobile[-10:]}"],  # ensure 91 prefix
        "templateId": TEMPLATE_ID
    }

    headers = {
        "Content-Type": "application/json",
        "apikey": str(COMBIRDS_API_KEY)
    }

    if not all([COMBIRDS_API_KEY, SENDER_ID, TEMPLATE_ID]):
        print("⚠️ Missing configuration. Set COMBIRDS_API_KEY, SENDER_ID, TEMPLATE_ID.")
        return False

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(COMBIRDS_API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                print("✅ SMS Sent Successfully:", response.text)
                return True
            else:
                print(f"❌ SMS Send Failed ({response.status_code}):", response.text)
                return False

    except httpx.RequestError as e:
        print("❌ Request Error:", e)
        return False
    except Exception as e:
        print("❌ Unexpected Error:", e)
        return False
