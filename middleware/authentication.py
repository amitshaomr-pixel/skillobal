import os
import uuid
import logging
from jose import JWTError, jwt

# ✅ Logger setup
logger = logging.getLogger("uvicorn")

# ✅ Load environment configuration safely
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")  # Default to HS256 if not set


def create_token(user_id: str) -> str:
    """
    Create a JWT token for the user.
    Includes basic error handling and validation.
    """
    try:
        if not JWT_SECRET:
            raise ValueError("JWT_SECRET is not set in environment variables.")

        # ✅ Supported algorithm validation
        supported_algorithms = JWT_ALGORITHM
        if JWT_ALGORITHM not in supported_algorithms:
            raise ValueError(f"Unsupported JWT algorithm: {JWT_ALGORITHM}")

        payload = {
            "user_id": user_id,
            "nonce": str(uuid.uuid4())
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    except Exception as e:
        logger.error(f"❌ Token creation failed: {e}")
        raise


def decode_token(token: str) -> dict | None:
    """
    Decode and validate JWT token.
    Returns payload if valid, None if invalid or expired.
    """
    try:
        if not JWT_SECRET:
            logger.error("JWT_SECRET is not set in environment variables.")
            return None

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload

    except JWTError as e:
        logger.warning(f"⚠️ Token verification failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None
