from fastapi import APIRouter, HTTPException, Depends
from core.database import hero_collection
from login.token_utils import check_token


router = APIRouter(tags=["Hero Section"])

@router.get("/hero-section", dependencies=[Depends(check_token)])
async def get_hero_section():
    """Fetch the hero section details"""
    hero = await hero_collection.find_one({})
    if not hero:
        raise HTTPException(status_code=404, detail="Hero section not found")

    # Convert ObjectId to string
    hero["_id"] = str(hero["_id"])
    
    return {'data': hero}
