from typing import Dict, Any, List


def all_course_helper(course: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a MongoDB course document into a clean dict for API responses.
    """
    return {
        "id": str(course["_id"]),
        "title": course.get("title", ""),
        "description": course.get("description", ""),
        "course_image_url": course.get("course_image_url", ""),
        "rating": course.get("rating", 0),
        "instructor_id": str(course.get("instructor_id", "")),
        "category_id": str(course.get("category_id", "")),
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


def category_helper(category: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a MongoDB category document into a clean dict.
    """
    return {
        "id": str(category["_id"]),
        "title": category.get("title", ""),
        "description": category.get("description", ""),
        "image_url": category.get("image_url", ""),
        "rating": category.get("rating", 0),
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
