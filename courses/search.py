from fastapi import APIRouter, Depends, Query
from courses.logic.search_logic import search_courses_service
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   

router = APIRouter(tags=["Search"])


@router.get("/search", dependencies=[Depends(check_token)])
async def search_courses(
    query: str = Query(..., min_length=1),
    category_id: str | None = None
):

    courses, error = await search_courses_service(query, category_id)

    if error == "invalid_category":
        raise CustomError("Invalid category id", 400)

    if error == "not_found":
        raise CustomError("No courses found", 404)

    return {
        "data": courses
    }
