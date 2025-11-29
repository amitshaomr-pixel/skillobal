from fastapi import APIRouter, Depends
from contact.logic.contact_logic import fetch_contact
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # <-- ADD THIS

router = APIRouter(tags=["Contact"])


@router.get("/contact", dependencies=[Depends(check_token)])
async def get_contact():
    contact = await fetch_contact()

    if not contact:
        raise CustomError("Contact info not found", 404)   # <-- UPDATED

    return contact
