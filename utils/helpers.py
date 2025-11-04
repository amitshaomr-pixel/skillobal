def all_course_helper(course) -> dict:
    return {
        "id": str(course["_id"]),
        "title": course["title"],
        "description": course["description"],
        "image_url": course["image_url"],
        "rating": course["rating"],
        "instructor": course["instructor"],
        "cat_id": str(course["cat_id"])
    }

def course_helper(course) -> dict:
    return {
        "id": str(course["_id"]),
        "title": course["title"],
        "description": course["description"],
        "image_url": course["image_url"],
        "rating": course["rating"],
        "price": course["price"],
        "instructor_id": str(course.get("instructor_id","")),
        "cat_id": str(course["cat_id"]),
        "thumbnail_img_url": course.get("thumbnail_img_url", ""),
        "thumbnail_video_url": course.get("thumbnail_video_url", "")
    }
