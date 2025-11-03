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
        "instructor": course["instructor"],
        "cat_id": str(course["cat_id"])
    }
