from bson import ObjectId
from database.database import (
    users_collection,
    courses_collection,
    instructor_collection,
    languages_collection,
)
from utils.helpers import all_course_helper


async def get_recommended_courses(user_id: str, limit: str | None = None):
    
    # Fetch the user
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None, "User not found"

    # Get selected category IDs
    selected_categories = user.get("selected_categories", [])
    
    # Convert IDs to ObjectId list
    category_ids = [ObjectId(str(cat)) for cat in selected_categories]

    # Query courses with matching category IDs
    query = {"category_id": {"$in": category_ids}}

    # Handle limit
    limit_value = 0 if not limit else 2

    cursor = courses_collection.find(query).limit(limit_value)

    recommended_list = []

    async for course in cursor:

        # Fetch instructor details
        instructor = await instructor_collection.find_one(
            {"_id": ObjectId(course["instructor_id"])}
        )

        # Fetch language details
        language = await languages_collection.find_one(
            {"_id": ObjectId(course["language_id"])}
        )

        # Generate final cleaned response
        course_data = all_course_helper(course, instructor, language)

        recommended_list.append(course_data)

    return recommended_list, None
