from fastapi import Request, HTTPException, status
from middleware.authentication import decode_token
from database.database import users_collection
from bson import ObjectId

async def check_token(request: Request):
    """
    All-rounder token validator:
    Checks MongoDB user ID instead of static data.
    """
    # 1️⃣ Bearer token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        # 2️⃣ Custom header
        token = request.headers.get("token")
        if not token:
            # 3️⃣ Query param
            token = request.query_params.get("token")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing"
                )
    # Verify token
    payload = decode_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_identifier = payload["user_id"]
    user = None
    # Check MongoDB user exists
    if not user and "@" in user_identifier:
        user = await users_collection.find_one({"email": payload["user_id"]})

    if not user and user_identifier.isdigit():
        user = await users_collection.find_one({"mobile": user_identifier})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return {"user_id": payload["user_id"], "user": user}
