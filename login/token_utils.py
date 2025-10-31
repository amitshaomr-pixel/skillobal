from fastapi import Request, HTTPException, status
from core.authentication import verify_token
from core.database import users_collection


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
    print("Token received from frontend:", token)
    # Verify token
    payload = verify_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    print("Payload extracted from token:", payload)
    # Check MongoDB user exists
    user = users_collection.find_one({"_id": payload["user_id"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return {"user_id": payload["user_id"], "user": user}
