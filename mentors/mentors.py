from fastapi import APIRouter, Depends
from mentors.logic.mentors_logic import fetch_all_mentors
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # ✅ use this

router = APIRouter(tags=["Mentors"])


@router.get("/mentors", dependencies=[Depends(check_token)])
async def get_all_mentors():

    mentors, error = await fetch_all_mentors()

    if error == "not_found":
        raise CustomError("No mentors found", 404)   # ✅ updated

    return {
        "title": "Meet Our Professional Mentor",
        "subtitle": "Our mentors are professionals with years of experience in their fields, dedicated to helping you reach your learning goals.",
        "data": mentors
    }
