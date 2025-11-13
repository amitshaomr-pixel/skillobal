from fastapi import APIRouter, Depends, HTTPException, Query
from middleware.token_verification import check_token
from database.database import courses_collection, layout_collection
from utils.helpers import all_course_helper
from bson import ObjectId

router = APIRouter(tags=["Featured Courses"])

@router.get("/featured-courses", dependencies=[Depends(check_token)])
async def get_featured_courses(cat_id: str | None = None):
    """
    Fetch all featured courses (filtered by category if provided).
    """
    try:
        layout_id = ObjectId("68d104bd896833b9498ad494")  # ✅ Hardcoded layout ID
        layout_doc = await layout_collection.find_one({"_id": layout_id})

        if not layout_doc or "linked_courses" not in layout_doc:
            return {
                "title": "Our Featured Courses",
                "subtitle": "Explore our most in-demand courses to boost your skills and career.",
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
            "title": "Our Featured Courses",
            "subtitle": "Explore our most in-demand courses to boost your skills and career.",
            "data": courses
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching featured courses: {str(e)}")
    
    

@router.get("/search", dependencies=[Depends(check_token)])
async def search_courses(query: str = Query(..., min_length=1)):
    """
    Search featured courses by title or description.
    """
    try:
        cursor = courses_collection.find({
            "visible": True,
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        })

        courses = [all_course_helper(c) async for c in cursor]

        if not courses:
            raise HTTPException(status_code=404, detail="No courses found for this search")

        return courses

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
