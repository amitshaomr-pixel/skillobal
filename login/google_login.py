import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from database.database import users_collection
from middleware.authentication import create_token
from middleware.exceptions import CustomError
from dotenv import load_dotenv
from utils.helpers import serialize_user 
load_dotenv()

router = APIRouter(tags=["Firebase Login"])


def ensure_firebase_initialized() -> None:
    if firebase_admin._apps:
        return

    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

    try:
        if firebase_credentials:
            cred = credentials.Certificate(json.loads(firebase_credentials))
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    except Exception as exc:
        raise CustomError(f"Failed to initialize Firebase Admin: {exc}", 500)


@router.post("/google-login")
async def firebase_login(request: Request) -> JSONResponse:
    ensure_firebase_initialized()

    data = await request.json()
    firebase_token = data.get("access_token")

    if not firebase_token:
        raise CustomError("Firebase access token is required", 400)

    try:
        decoded_token = auth.verify_id_token(firebase_token)

    except Exception as e:
        raise CustomError(f"Invalid Firebase token: {str(e)}", 401)

    # Google user data
    google_user = {
        "name": decoded_token.get("name"),
        "email": decoded_token.get("email"),
        "profile_image": decoded_token.get("picture", "https://cdn-icons-png.flaticon.com/512/149/149071.png"),
        "mobile": data.get("mobile", 0)
    }


    existing_user = await users_collection.find_one({"email": google_user["email"]})

    if existing_user:
        user_db = existing_user

    else:
        await users_collection.insert_one(google_user)
        user_db = await users_collection.find_one({"email": google_user["email"]})

    user_response = await serialize_user(user_db)
    token = create_token(str(user_db["_id"]))

    return JSONResponse({
        "status": "Success",
        "message": "Login Successful",
        "user": user_response,
        "token": token
    })
