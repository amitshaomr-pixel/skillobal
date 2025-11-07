from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from login.token_utils import check_token
from core.database import courses_collection

router = APIRouter(tags=["Course Review"])

# 🧩 Review Schema
class Review(BaseModel):
    user_id: str
    username: str
    rating: float
    comment: str
    profile_image: str  # URL or base64 string

# 🚀 Post Review for the same course_id
@router.post("/courses-detail/{course_id}/add-review", dependencies=[Depends(check_token)])
async def add_review_to_course(course_id: str, review: Review):
    try:
        # Validate course_id
        try:
            course_oid = ObjectId(course_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid course id")

        # Check if course exists
        course = await courses_collection.find_one({"_id": course_oid})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Add the review to the course
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
