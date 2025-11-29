from fastapi import APIRouter, Depends
from pydantic import BaseModel
from middleware.exceptions import CustomError
from courses.logic.review_logic import add_review
from middleware.token_verification import check_token

router = APIRouter(tags=["Course Review"])


class Review(BaseModel):
    user_id: str
    username: str
    rating: float
    comment: str
    profile_image: str


@router.post("/courses-detail/{course_id}/add-review", dependencies=[Depends(check_token)])
async def add_review_to_course(course_id: str, review: Review):

    result, error = await add_review(course_id, review.dict())

    if error == "invalid_id":
        raise CustomError("Invalid course id", 400)

    if error == "not_found":
        raise CustomError("Course not found", 404)

    return {
        "status": "success",
        "message": "Review added successfully",
        "course_id": course_id,
        "review": result
    }
