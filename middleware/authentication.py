from fastapi import Header
import os
import uuid
import logging
from jose import JWTError, jwt
from middleware.exceptions import CustomError   # ✅ unified custom error

logger = logging.getLogger("uvicorn")

# Load environment configuration
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")   # default HS256

# Allowed algorithms
SUPPORTED_ALGORITHMS = ["HS256", "HS384", "HS512"]


def create_token(user_id: str) -> str:
    """
    Create a JWT token for the user.
    """
    try:
        if not JWT_SECRET:
            raise CustomError("JWT_SECRET is not set in environment variables.", 500)

        if JWT_ALGORITHM not in SUPPORTED_ALGORITHMS:
            raise CustomError(
                f"Unsupported JWT algorithm: {JWT_ALGORITHM}. Allowed: {SUPPORTED_ALGORITHMS}",
                500
            )

        payload = {
            "user_id": user_id,
            "nonce": str(uuid.uuid4())
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    except CustomError:
        raise
    except Exception as e:
        logger.error(f"Token creation failed: {e}")
        raise CustomError("Failed to generate authentication token", 500)


def decode_token(token: str) -> dict | None:
    """
    Decode and verify JWT token.
    Returns: decoded payload or None if invalid.
    """
    try:
        if not JWT_SECRET:
            logger.error("JWT_SECRET is not set in environment variables.")
            return None

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload

    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None




async def optional_auth(authorization: str = Header(default=None)):
    if authorization is None:
        return None   # <-- IMPORTANT

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        return payload
    except:
        return None   # <-- ALSO IMPORTANT