from fastapi import APIRouter, Depends, HTTPException
from middleware.token_verification import check_token
from database.database import courses_collection, layout_collection
from utils.helpers import all_course_helper
from bson import ObjectId

router = APIRouter(tags=["Popular Courses"])

@router.get("/popular-courses", dependencies=[Depends(check_token)])
async def get_popular_courses(cat_id: str | None = None):
    """
    Fetch all popular courses (filtered by category if provided).
    """
    try:
        layout_id = ObjectId("68d0d3643deb5b22c6613b61")  # ✅ Hardcoded layout ID
        layout_doc = await layout_collection.find_one({"_id": layout_id})

        if not layout_doc or "linked_courses" not in layout_doc:
            return {
                "title": "Our Popular Courses",
                "subtitle": "Level up your skills with our most popular and trending courses.",
                "data": []
            }

        linked_courses = layout_doc["linked_courses"]

        query = {"_id": {"$in": linked_courses}, "visible": True}

        if cat_id:
            if not ObjectId.is_valid(cat_id):
                raise HTTPException(status_code=400, detail="Invalid category id")
            query["cat_id"] = ObjectId(cat_id)

        courses = [all_course_helper(c) async for c in courses_collection.find(query)]

        return {
            "title": "Our Popular Courses",
            "subtitle": "Level up your skills with our most popular and trending courses.",
            "data": courses
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching popular courses: {str(e)}")
