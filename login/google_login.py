from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from google.oauth2 import id_token
import google.auth.transport.requests
from core.database import users_collection
from core.authentication import create_token
import os

router = APIRouter(tags=["Firebase Login"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@router.post("/google-login")
async def firebase_login(request: Request):
    """
    Verifies Firebase ID token from frontend,
    extracts user details, saves/updates them in DB,
    and returns app login token.
    """
    data = await request.json()
    firebase_token = data.get("access_token")

    if not firebase_token:
        raise HTTPException(status_code=400, detail="Firebase access token is required")

    try:
        # Verify the Firebase token
        id_info = id_token.verify_oauth2_token(
            firebase_token,
            google.auth.transport.requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Extract user info
        user_data = {
            "name": id_info.get("name"),
            "email": id_info.get("email"),
            "picture": id_info.get("picture"),
            "uid": id_info.get("sub"),  # Firebase unique user ID
        }

        # Store or update user in MongoDB
        await users_collection.update_one(
            {"email": user_data["email"]},
            {"$set": user_data},
            upsert=True
        )

        # Generate app-specific JWT token
        app_token = create_token(user_data["email"])

        return JSONResponse({
            "status": "success",
            "user": user_data,
            "token": app_token
        })

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {e}")