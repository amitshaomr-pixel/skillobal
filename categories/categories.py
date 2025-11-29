from fastapi import APIRouter, Depends
from categories.logic.categories_logic import fetch_all_categories, fetch_courses_by_category
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # <-- ADD THIS

router = APIRouter(tags=["Categories"])


@router.get("/categories", dependencies=[Depends(check_token)])
async def get_categories(limit: str | None = None):

    categories = await fetch_all_categories()

    if not categories:
        raise CustomError("No categories found", 404)   # <-- UPDATED

    if not limit:
        limit_value = 0
    else:
        limit_value = 5

    final_data = categories[:limit_value] if limit_value > 0 else categories

    return {
        "title": "Categories",
        "subtitle": (
            "Our mentors are professionals with years of experience in their fields, "
            "dedicated to helping you reach your learning goals."
        ),
        "data": final_data
    }


@router.get("/categories/{category_id}", dependencies=[Depends(check_token)])
async def get_courses_by_category(category_id: str):

    courses, error = await fetch_courses_by_category(category_id)

    if error == "invalid_id":
        raise CustomError("Invalid category ID", 400)  

    if not courses:
        raise CustomError("No courses found for this category", 404) 

    return {
        "category_id": category_id,
        "data": courses
    }
