from fastapi import APIRouter, HTTPException, Depends
from core.database import categories_collection
from login.token_utils import check_token
from utils.helpers import all_course_helper
from core.database import courses_collection
from bson import ObjectId

router = APIRouter(tags=["Popular Categories"])

@router.get("/categories", dependencies=[Depends(check_token)])
async def get_popular_categories():
    """Fetch list of all categories with main title and subtitle"""
    
    categories = []
    async for cat in categories_collection.find({}):
        categories.append({
            "id": str(cat["_id"]),
            "title": cat.get("name", "Untitled Category"),
            "subtitle": cat.get("description", "No description available."),
            "image_url": cat.get("image_url", "")
        })
    
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return {
        "title": "Categories",
        "subtitle": "Our mentors are professionals with years of experience in their fields, dedicated to helping you reach your learning goals.",
        "data": categories
    }




@router.get("/categories/{cat_id}", dependencies=[Depends(check_token)])
async def get_courses_by_category(cat_id: str):
    """Fetch all courses that belong to a specific category"""
    try:
        oid = ObjectId(cat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category id")

    courses = []
    async for course in courses_collection.find({"cat_id": oid, "visible": True}):
        courses.append(all_course_helper(course))

    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for this category")

    return {
        "category_id": cat_id,
        "Data": courses
    }