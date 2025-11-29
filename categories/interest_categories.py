from fastapi import APIRouter, Depends
from middleware.token_verification import check_token
from models.interest_categories_schema import InterestCategoryRequest
from categories.logic.interest_categories_logic import save_interest_categories

router = APIRouter(tags=["Select Categories"])


@router.post("/interest-categories")
async def select_interest_categories(payload: InterestCategoryRequest, user=Depends(check_token)):
    user_id = user.get("user_id")

    # Now get category id + name from logic function
    categories = await save_interest_categories(
        user_id=user_id,
        category_ids=payload.category_ids
    )

    return {
        "message": "Selected categories updated successfully",
        "data": categories
    }