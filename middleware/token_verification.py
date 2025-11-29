from fastapi import Request
from middleware.authentication import decode_token
from database.database import users_collection
from bson import ObjectId
from middleware.exceptions import CustomError   # ✅ use this

async def check_token(request: Request):

    # Get token
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        # Try alternate sources
        token = request.headers.get("token") or request.query_params.get("token")
        if not token:
            raise CustomError("Token missing", 401)   # ✅ updated

    # Decode
    payload = decode_token(token)
    if not payload or "user_id" not in payload:
        raise CustomError("Invalid token", 401)   # ✅ updated

    user_identifier = payload["user_id"]
    user = None

    # Look up by ObjectId
    if ObjectId.is_valid(user_identifier):
        user = await users_collection.find_one({"_id": ObjectId(user_identifier)})

    if not user:
        raise CustomError("User not found", 401)   # ✅ updated

    return {
        "user_id": str(user["_id"]),
        "user": user
    }
