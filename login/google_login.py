import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from database.database import users_collection
from middleware.authentication import create_token
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Firebase Login"])

def ensure_firebase_initialized() -> None:
    """
    Initialize Firebase Admin SDK once per process.
    Tries JSON credentials from FIREBASE_CREDENTIALS, falling back to ADC if absent.
    """
    if firebase_admin._apps:
        return
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    try:
        if firebase_credentials:
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        else:
            # Attempts to initialize with Application Default Credentials (ADC)
            firebase_admin.initialize_app()
    except Exception as exc:
        # Surface a clear configuration error
        raise RuntimeError(f"Failed to initialize Firebase Admin: {exc}") from exc


@router.post("/google-login")
async def firebase_login(request: Request) -> JSONResponse:
    """
    Verifies Firebase ID token from frontend,
    extracts user details, saves/updates them in DB,
    and returns app login token.
    """
    # Ensure Firebase is initialized
    try:
        ensure_firebase_initialized()
    except Exception as init_exc:
        raise HTTPException(status_code=500, detail=str(init_exc))
    data = await request.json()
    firebase_token = data.get("access_token")

    if not firebase_token:
        raise HTTPException(status_code=400, detail="Firebase access token is required")

    try:
        # ✅ Verify Firebase token properly
        decoded_token = auth.verify_id_token(firebase_token)
        user_data = {
            "name": decoded_token.get("name"),
            "email": decoded_token.get("email"),
            "picture": decoded_token.get("picture"),
            
        }

        # Store/update in MongoDB
        await users_collection.update_one(
            {"email": user_data["email"]},
            {"$set": user_data},
            upsert=True
        )

        # Create app token
        app_token = create_token(user_data["email"])

        return JSONResponse({
            "status": "success",
            "message":"Login Successfull",
            "user": user_data,
            "token": app_token
        })

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")
