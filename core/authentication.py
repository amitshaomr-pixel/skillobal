
from jose import JWTError, jwt
import uuid

# Secret key and algorithm
JWT_SECRET = "Xq7!r$T9vB2y@Hk6M8p#Ln3jW1zC5dAa"
JWT_ALGORITHM = "HS256"

def create_token(user_id: str) -> str:
    """
    Create a JWT token with the MongoDB user ID.
    No expiration.
    """
    payload = {
        "user_id": user_id,
        "nonce": str(uuid.uuid4())
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str) -> dict | None:
    """
    Verify JWT token.
    Returns payload dict if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
