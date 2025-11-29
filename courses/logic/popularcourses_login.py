from bson import ObjectId
from database.database import (
    layout_collection,
    courses_collection,
    instructor_collection,
    languages_collection
)
from utils.helpers import all_course_helper


LAYOUT_ID = ObjectId("68d0d3643deb5b22c6613b61")   # hardcoded layout ID


async def fetch_popular_courses(limit: str | None = None):

    # Fetch layout
    layout_doc = await layout_collection.find_one({"_id": LAYOUT_ID})
    if not layout_doc or "linked_courses" not in layout_doc:
        return [], None  

    linked_courses = layout_doc["linked_courses"]

    query = {
        "_id": {"$in": linked_courses},
        "visible": True
    }

    limit_value = 0 if not limit else 2

    cursor = courses_collection.find(query).limit(limit_value)
    raw_courses = [c async for c in cursor]

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

        # Build final course object
        course_data = all_course_helper(
            course,
            instructor,
            language
        )

        final_courses.append(course_data)

    return final_courses, None
