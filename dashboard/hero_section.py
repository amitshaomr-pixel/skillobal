from fastapi import APIRouter, Depends
from middleware.token_verification import check_token
from dashboard.logic.logic import fetch_hero_section
from middleware.exceptions import CustomError   # ✅ use custom error

router = APIRouter(tags=["Hero Section"])


@router.get("/hero-section", dependencies=[Depends(check_token)])
async def get_hero_section():

    hero_data, error = await fetch_hero_section()

    if error == "not_found":
        raise CustomError("Hero section not found", 404)   # ✅ updated

    return {"data": hero_data}
