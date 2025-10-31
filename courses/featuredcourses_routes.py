from fastapi import APIRouter, Query, Depends, HTTPException
from login.token_utils import check_token
from core.database import courses_collection, layout_collection
from utils.helpers import all_course_helper
from bson import ObjectId


router = APIRouter(tags=["Featured Courses"]) 


@router.get("/all-featured-courses", dependencies=[Depends(check_token)])
async def get_featured_courses(cat_id: str | None = None):
    layout_id = ObjectId("68d104bd896833b9498ad494")
    layout_doc = await layout_collection.find_one({"_id": layout_id})

    if not layout_doc or "linked_courses" not in layout_doc:
        return {
            "title": "Our Featured Courses",
            "subtitle": "Explore our most in-demand courses to boost your skills and career.",
            "data": []
        }

    linked_courses = layout_doc["linked_courses"]

    query = {
        "_id": {"$in": linked_courses},
        "visible": True
    }

    if cat_id:
        try:
            query["cat_id"] = ObjectId(cat_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid category id")

    courses = []
    async for course in courses_collection.find(query):
        courses.append(all_course_helper(course))

    return {
        "title": "Our Featured Courses",
        "subtitle": "Explore our most in-demand courses to boost your skills and career.",
        "data": courses
    }





@router.get("/search",  dependencies=[Depends(check_token)])
async def search_courses(query: str = Query(..., min_length=1)):
    """
    Search popular courses by title or description
    """
    courses = []
    cursor = courses_collection.find({
        "visible": True,
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]                           
    })
    async for course in cursor:
        courses.append(all_course_helper(course))
    
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for this search")
    
    return courses  
