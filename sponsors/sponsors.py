from fastapi import APIRouter, Depends
from sponsors.logic.sponsors_logic import fetch_all_sponsors
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # ✅ use this

router = APIRouter(tags=["Sponsors"])


@router.get("/sponsors", dependencies=[Depends(check_token)])
async def get_sponsors():
    """Fetch the sponsors details"""

    sponsors, error = await fetch_all_sponsors()

    if error == "not_found":
        raise CustomError("No sponsors found", 404)   # ✅ replaced HTTPException

    return {
        "title": "Our Learning Sponsors",
        "data": sponsors
    }
