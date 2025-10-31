import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

courses_collection = db["courses"]
users_collection = db["users"]
layout_collection = db["layout"]
slider_collection = db["sliders"]
hero_collection = db["dashboard"]
sponsors_collection = db["sponsors"]
categories_collection = db["categories"]
mentors_collection = db["mentors"]
testimonials_collection = db["testimonials"]
faqs_collection = db["Q&A"]
contact_collection = db["contact"]