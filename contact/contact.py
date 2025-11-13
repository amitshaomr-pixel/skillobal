from fastapi import APIRouter, HTTPException, Depends
from database.database import contact_collection
from middleware.token_verification import check_token

router = APIRouter(tags=["Contact"])

@router.get("/contact",dependencies=[Depends(check_token)])
async def get_contact():
    contact = await contact_collection.find_one()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact info not found")
    contact["_id"] = str(contact["_id"])
    return contact