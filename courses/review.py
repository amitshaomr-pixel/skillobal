from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from middleware.token_verification import check_token
from database.database import courses_collection

router = APIRouter(tags=["Course Review"])

class Review(BaseModel):
    user_id: str
    username: str
    rating: float
    comment: str
    profile_image: str  # URL or base64 string

@router.post("/courses-detail/{course_id}/add-review", dependencies=[Depends(check_token)])
async def add_review_to_course(course_id: str, review: Review):
    """
    Add a review to a specific course.
    """
    try:
        if not ObjectId.is_valid(course_id):
            raise HTTPException(status_code=400, detail="Invalid course id")

        course_oid = ObjectId(course_id)
        course = await courses_collection.find_one({"_id": course_oid})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        await courses_collection.update_one(
            {"_id": course_oid},
            {"$push": {"reviews": review.dict()}}
        )

        return {
            "status": "success",
            "message": "Review added successfully",
            "course_id": course_id,
            "review": review.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding review: {str(e)}")
