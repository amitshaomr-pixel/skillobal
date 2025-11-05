from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from core.database import users_collection
from core.authentication import create_token
import os

router = APIRouter(tags=["Google Auth"])

# Allow insecure transport (for localhost only)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET_FILE = "core/client_secret.json"


# ---------------------- Google OAuth Flow ---------------------- #
def get_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ],
        redirect_uri="http://127.0.0.1:8000/auth/callback"
    )


# ---------------------- Step 1: Redirect to Google ---------------------- #
@router.get("/google-auth")
async def google_auth():
    """
    Redirect user to Google account selection page.
    """
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt="select_account")  # Always show email chooser
    return RedirectResponse(auth_url)


# ---------------------- Step 2: Handle Callback ---------------------- #
@router.get("/auth/callback")
async def callback(request: Request):
    """
    Handle redirect from Google OAuth.
    """
    flow = get_flow()
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    print("Google ID Token:", credentials._id_token)

    token_request = google.auth.transport.requests.Request()

    try:
        id_info = id_token.verify_oauth2_token(
            credentials._id_token, token_request, GOOGLE_CLIENT_ID
        )

        # Extract and save user info
        user_data = {
            "name": id_info.get("name"),
            "email": id_info.get("email"),
            "picture": id_info.get("picture"),
        }

        await users_collection.update_one(
            {"email": user_data["email"]},
            {"$set": user_data},
            upsert=True
        )

        # Generate app JWT
        app_token = create_token({"email": user_data["email"]})

        # ✅ Return JSON (you can redirect to frontend if needed)
        return JSONResponse({
            "status": "success",
            "user": user_data,
            "token": app_token
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
