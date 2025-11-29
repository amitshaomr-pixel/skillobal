from bson import ObjectId
from database.database import courses_collection, courses_videos_collection
from utils.helpers import course_helper


async def fetch_course_detail(course_id: str):

    # Validate course_id
    if not ObjectId.is_valid(course_id):
        return None, "invalid_id"

    course_oid = ObjectId(course_id)

    # Fetch course
    course = await courses_collection.find_one({"_id": course_oid})
    if not course:
        return None, "not_found"

    course_data = course_helper(course)

    # Extract linked video id
    video_id = course.get("videos")

    # If no video linked or invalid → return no videos
    if not video_id or not ObjectId.is_valid(str(video_id)):
        course_data["videos"] = []
        return course_data, None

    # Fetch video document
    video_doc = await courses_videos_collection.find_one(
        {"_id": ObjectId(video_id)},
        {
            "videos.video_title": 1,
            "videos.video_description": 1,
            "videos.videoUrl": 1,
            "videos.order": 1,
            "videos.type": 1
        }
    )

    # No videos found
    if not video_doc:
        course_data["videos"] = []
        return course_data, None

    # Attach video list
    course_data["videos"] = video_doc.get("videos", [])
    return course_data, None
