from bson import ObjectId
from database.database import (
    courses_collection,
    instructor_collection,
    languages_collection,
)
from utils.helpers import all_course_helper


async def search_courses_service(query: str, category_id: str | None = None):

    # Base search query
    filter_query = {
        "visible": True,
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
        ],
    }

    # If query looks like ObjectId → include _id and category_id in OR search
    try:
        oid = ObjectId(query)
        filter_query["$or"].append({"_id": oid})
        filter_query["$or"].append({"category_id": oid})
    except Exception:
        pass

    # Category filtering
    if category_id:
        if not ObjectId.is_valid(category_id):
            return None, "invalid_category"

        filter_query["category_id"] = ObjectId(category_id)

    # Fetch raw courses
    cursor = courses_collection.find(filter_query)
    raw_courses = [c async for c in cursor]

    if not raw_courses:
        return None, "not_found"

    final_courses = []

    for course in raw_courses:

        # Fetch instructor details
        instructor = await instructor_collection.find_one(
            {"_id": ObjectId(course["instructor_id"])}
        )

        # Fetch language details
        language = await languages_collection.find_one(
            {"_id": ObjectId(course["language_id"])}
        )

        # Prepare final course response
        course_data = all_course_helper(course, instructor, language)

        final_courses.append(course_data)

    return final_courses, None
