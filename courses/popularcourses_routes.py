from fastapi import APIRouter,Depends
from login.token_utils import *
from core.database import courses_collection , layout_collection , slider_collection
from utils.helpers import all_course_helper
from bson import ObjectId
 
router = APIRouter(tags=["All Popular Courses"])


@router.get("/all-popular-courses", dependencies=[Depends(check_token)])
async def get_popular_courses(cat_id: str | None = None):
    layout_id = ObjectId("68d0d3643deb5b22c6613b61")
    layout_doc = await layout_collection.find_one({"_id": layout_id})
    
    if not layout_doc or "linked_courses" not in layout_doc:
        return {
            "title": "Our Popular Courses",
            "subtitle": "Level up your skills with our most popular and trending courses.",
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
        "title": "Our Popular Courses",
        "subtitle": "Level up your skills with our most popular and trending courses.",
        "data": courses
    }




SLIDER_PROJECTION = {
    "img_url": 1,
    "title": 1,
    "description": 1,
    "cat_id":1,
    'datetime':0
}

@router.get("/sliders" , dependencies=[Depends(check_token)])
async def get_sliders():
    sliders = []
    async for doc in slider_collection.find({}, SLIDER_PROJECTION):
        doc["_id"] = str(doc["_id"])  
        if "cat_id" in doc and doc["cat_id"]:  
            doc["cat_id"] = str(doc["cat_id"])
        sliders.append(doc)
    return sliders

