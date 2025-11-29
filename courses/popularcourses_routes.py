from fastapi import APIRouter, Depends
from courses.logic.popularcourses_login import fetch_popular_courses
from middleware.token_verification import check_token
from middleware.exceptions import CustomError  # <-- Added

router = APIRouter(tags=["Popular Courses"])


@router.get("/popular-courses", dependencies=[Depends(check_token)])
async def get_popular_courses(limit: str | None = None):

    courses, error = await fetch_popular_courses(limit)

    if error == "invalid_id":
        raise CustomError("Invalid category id", 400)  # <-- updated

    return {
        "title": "Our Popular Courses",
        "subtitle": "Level up your skills with our most popular and trending courses.",
        "api_url": "popular-courses",
        "data": courses or []
    }
