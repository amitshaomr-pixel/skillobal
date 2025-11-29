from fastapi import APIRouter, Depends
from comments.logic.testimonials_logic import fetch_all_testimonials
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # <-- ADD THIS

router = APIRouter(tags=["Testimonials"])


@router.get("/testimonials", dependencies=[Depends(check_token)])
async def get_testimonials():

    testimonials = await fetch_all_testimonials()

    if not testimonials:
        raise CustomError("No testimonials found", 404)   # <-- UPDATED

    return {
        "title": "Testimonials",
        "subtitle": "Here's what people are saying",
        "data": testimonials
    }
