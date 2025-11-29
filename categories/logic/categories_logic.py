from database.database import categories_collection, courses_collection
from utils.helpers import category_helper
from bson import ObjectId


async def fetch_all_categories():
    categories = []

    async for cat in categories_collection.find({}):
        categories.append(category_helper(cat))

    return categories


async def fetch_courses_by_category(category_id: str):
    try:
        oid = ObjectId(category_id)
    except Exception:
        return None, "invalid_id"

    courses = []
    async for course in courses_collection.find({"category_id": oid, "visible": True}):
        courses.append({
            "id": str(course["_id"]),
            "title": course.get("title", ""),
            "description": course.get("description", ""),
            "course_image_url": course.get("course_image_url", ""),
            "rating": course.get("rating", 0)
        })

    return courses, None

