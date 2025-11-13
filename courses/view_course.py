from fastapi import APIRouter, Depends, HTTPException
from middleware.token_verification import check_token
from database.database import courses_collection, courses_videos_collection
from utils.helpers import course_helper
from bson import ObjectId

router = APIRouter(tags=["View Course"])

@router.get("/courses-detail/{course_id}", dependencies=[Depends(check_token)])
async def get_course_detail(course_id: str):
    """
    Fetch full course details along with video data.
    """
    try:
        if not ObjectId.is_valid(course_id):
            raise HTTPException(status_code=400, detail="Invalid course id")

        course = await courses_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        course_data = course_helper(course)
        video_id = course.get("videos")

        if not video_id or not ObjectId.is_valid(str(video_id)):
            course_data["videos"] = []
            return {"status": "success", "data": course_data}

        video_doc = await courses_videos_collection.find_one(
            {"_id": ObjectId(video_id)},
            {"videos.video_title": 1, "videos.video_description": 1, "videos.videoUrl": 1, "videos.order": 1, "videos.type": 1}
        )

        if not video_doc:
            course_data["videos"] = []
            return {"status": "success", "data": course_data}

        course_data["videos"] = video_doc.get("videos", [])
        return {"status": "success", "data": course_data}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching course detail: {str(e)}")
