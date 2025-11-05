from fastapi import APIRouter, Depends, HTTPException
from login.token_utils import check_token
from core.database import courses_collection, instructor_collection
from utils.helpers import course_helper
from bson import ObjectId

router = APIRouter(tags=["View Course"])

@router.get("/courses-detail/{course_id}", dependencies=[Depends(check_token)])
async def get_course_detail(course_id: str):
    """
    Fetch full course details including instructor and video data.
    """
    try:
        oid = ObjectId(course_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid course id")

    # Fetch course document
    course = await courses_collection.find_one({"_id": oid})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Format basic course data
    course_data = course_helper(course)

    # Fetch instructor data using instructor_id
    instructor_data = None
    instructor_id = course.get("instructor_id")
    if instructor_id:
        try:
            instructor_oid = ObjectId(instructor_id)
            instructor = await instructor_collection.find_one({"_id": instructor_oid})
            if instructor:
                instructor["_id"] = str(instructor["_id"])
                instructor_data = instructor
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid instructor id")

    # Add instructor info
    course_data["instructor"] = instructor_data

    # Add videos list from course document
    videos = course.get("videos", [])
    course_data["lessons"] = videos

    return {"status": "success", "data": course_data}

