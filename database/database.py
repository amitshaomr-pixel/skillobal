import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# ✅ Logger setup
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# ✅ Connection setup with pooling and error handling
try:
    client = AsyncIOMotorClient(
        MONGO_URI,
        maxPoolSize=20,          # ✅ Connection pool limit
        minPoolSize=5,           # ✅ Minimum connections
        serverSelectionTimeoutMS=5000  # ✅ Timeout for connection
    )
    db = client[DB_NAME]
    logger.info(f"✅ Connected to MongoDB Database: {DB_NAME}")
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    db = None

# ✅ Collections
courses_collection = db["courses"]
users_collection = db["users"]
layout_collection = db["layout"]
slider_collection = db["sliders"]
hero_collection = db["dashboard"]
sponsors_collection = db["sponsors"]
categories_collection = db["categories"]
instructor_collection = db["instructor"]
testimonials_collection = db["testimonials"]
faqs_collection = db["Q&A"]
contact_collection = db["contact"]
courses_videos_collection = db["courses_videos"]

# ✅ Health Check Function
async def check_database_health() -> bool:
    """Check MongoDB connection status."""
    try:
        await client.admin.command("ping")
        return True
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")
        return False
