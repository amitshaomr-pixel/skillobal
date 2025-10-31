from fastapi import APIRouter, HTTPException, Depends
from core.database import sponsors_collection  # use your actual collection name
from login.token_utils import check_token

router = APIRouter(tags=["Sponsors"])

@router.get("/sponsors", dependencies=[Depends(check_token)])
async def get_sponsors():
    """Fetch the sponsors details"""
    sponsor_list = []

    async for sponsor in sponsors_collection.find({}):
        sponsor["_id"] = str(sponsor["_id"])  # Convert ObjectId to string
        sponsor_list.append(sponsor)

    if not sponsor_list:
        raise HTTPException(status_code=404, detail="No sponsors found")

    return {
        "title": "Our Learning Sponsors",
        "data": sponsor_list
    }
