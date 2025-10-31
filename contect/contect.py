from fastapi import APIRouter, HTTPException, Depends
from core.database import contact_collection
from login.token_utils import check_token

router = APIRouter(tags=["Contact"])

@router.get("/contact",dependencies=[Depends(check_token)])
async def get_contact():
    contact = await contact_collection.find_one()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact info not found")
    contact["_id"] = str(contact["_id"])
    return contact