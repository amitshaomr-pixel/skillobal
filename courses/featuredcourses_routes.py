from fastapi import APIRouter, Depends
from courses.logic.featuredcourses_logic import fetch_featured_courses
from middleware.token_verification import check_token
from middleware.exceptions import CustomError    # <-- Added

router = APIRouter(tags=["Featured Courses"])


@router.get("/featured-courses", dependencies=[Depends(check_token)])
async def get_featured_courses(limit: str | None = None):

    courses, error = await fetch_featured_courses(limit)

    if error == "invalid_id":
        raise CustomError("Invalid category id", 400)  # <-- updated

    return {
        "title": "Our Featured Courses",
        "subtitle": "Explore our most in-demand courses to boost your skills and career.",
        "api_url": "featured-courses",
        "data": courses or []
    }
