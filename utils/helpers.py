from typing import Dict, Any, List
from database.database import categories_collection

def all_course_helper(course,instructor,language) :
    """
    Transform a MongoDB course document into a clean dict for API responses.
    """
    return {
        "id": str(course["_id"]),
        "title": course.get("title", ""),
        "description": course.get("description", ""),
        "course_image_url": course.get("course_image_url", ""),
        "rating": course.get("rating", 0),
        "lessons": course.get("lessons",""),
        "instructor": (instructor.get("name", "")),
    }


def course_helper(course: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detailed course helper for individual course fetch.
    """
    return {
        "id": str(course["_id"]),
        "title": course.get("title", ""),
        "description": course.get("description", ""),
        "course_image_url": course.get("course_image_url", ""),
        "rating": course.get("rating", 0),
        "instructor_id": str(course.get("instructor_id", "")),
        "category_id": str(course.get("category_id", "")),
        "reviews": course.get("reviews", []),
    }


def category_helper(category):
    """
    Transform a MongoDB category document into a clean dict.
    """
    return {
        "id": str(category["_id"]),
        "name": category.get("name", ""),
        "image_url": category.get("image", {}).get("image_url", "") or category.get("image_url", ""),
    }


def video_helper(video: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a single video item into a clean dict.
    """
    return {
        "order": video.get("order", 0),
        "video_title": video.get("video_title", ""),
        "video_description": video.get("video_description", ""),
        "video_url": video.get("videoUrl", ""),
        "file_id": video.get("fileId", ""),
        "type": video.get("type", "video"),
    }


def videos_list_helper(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply video_helper to a list of videos.
    """
    return [video_helper(v) for v in videos]


async def serialize_user(user):
    """Convert MongoDB user -> JSON safe user with category details"""
    if not user:
        return None

    # Convert stored category ObjectIds into category documents
    category_oids = user.get("selected_categories", [])
    
    categories = []
    if category_oids:
        categories_cursor = categories_collection.find(
            {"_id": {"$in": category_oids}},
            {"name": 1}
        )
        categories_list = await categories_cursor.to_list(None)

        categories = [
            {
                "id": str(cat["_id"]),
                "name": cat.get("name", "")
            }
            for cat in categories_list
        ]

    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "mobile": user.get("mobile"),
        "gender": user.get("gender", "Select"),
        "profile_image": user.get("profile_image"),
        "selected_categories": categories
    }