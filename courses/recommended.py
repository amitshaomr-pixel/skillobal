from fastapi import APIRouter, Depends
from middleware.token_verification import check_token
from middleware.exceptions import CustomError  # <-- Added
from courses.logic.recommended_courses_logic import get_recommended_courses

router = APIRouter()


@router.get("/recommended-courses")
async def recommended_courses(current_user: dict = Depends(check_token), limit: str | None = None):
    user_id = current_user.get("user_id")

    courses, error = await get_recommended_courses(user_id, limit)

    if error:   # "User not found"
        raise CustomError(error, 404)  # <-- updated

    return {
        "title": "Recommended courses",
        "subtitle": "Level up your skills with our most popular and trending recommended courses.",
        "api_url": "recommended-courses",
        "data": courses
    }
