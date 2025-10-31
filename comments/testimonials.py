from fastapi import APIRouter, HTTPException, Depends
from core.database import testimonials_collection
from login.token_utils import check_token

router = APIRouter(tags=["Testimonials"])

@router.get("/testimonials",dependencies=[Depends(check_token)])
async def get_testimonials():
    """Fetch testimonial section data"""
    testimonials = []
    async for t in testimonials_collection.find({}):
        testimonials.append({
            "id": str(t["_id"]),
            "message": t.get("message"),
            "name": t.get("name"),
            "designation": t.get("designation"),
            "profile_image": t.get("profile_image")
        })

    if not testimonials:
        raise HTTPException(status_code=404, detail="No testimonials found")

    return {
        "title": "Testimonials",
        "subtitle": "Here's what people are saying",
        "data": testimonials
    }
