from bson import ObjectId
from database.database import courses_collection


async def add_review(course_id: str, review_data: dict):


    # Validate ObjectId
    if not ObjectId.is_valid(course_id):
        return None, "invalid_id"

    course_oid = ObjectId(course_id)

    # Check if course exists
    course = await courses_collection.find_one({"_id": course_oid})
    if not course:
        return None, "not_found"

    # Push review into array
    await courses_collection.update_one(
        {"_id": course_oid},
        {"$push": {"reviews": review_data}}
    )

    return review_data, None
