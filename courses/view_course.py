from fastapi import APIRouter, Depends, HTTPException
from login.token_utils import check_token
from core.database import courses_collection
from utils.helpers import course_helper
from bson import ObjectId

router = APIRouter(tags=["View Course"])

@router.get("/courses-id/{course_id}", dependencies=[Depends(check_token)])
async def get_featured_course_by_id(course_id: str):
    try:
        oid = ObjectId(course_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid course id")

    course = await courses_collection.find_one({"_id": oid})
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course_helper(course)
