from fastapi import APIRouter, HTTPException, Depends
from core.database import instructor_collection
from login.token_utils import check_token

router = APIRouter(tags=["Mentors"])

@router.get("/mentors", dependencies=[Depends(check_token)])
async def get_all_mentors():
    """Fetch mentor section data"""
    mentors = []
    async for mentor in instructor_collection.find({}):
        mentors.append({
            "id": str(mentor["_id"]),
            "name": mentor.get("name"),
            "role": mentor.get("role"),
            "experience": mentor.get("experience"),
            "image_url": mentor.get("image_url")
        })

    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found")

    return {
        "title": "Meet Our Professional Mentor",
        "subtitle": "Our mentors are professionals with years of experience in their fields, dedicated to helping you reach your learning goals.",
        "data": mentors
    }
