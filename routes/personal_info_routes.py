from fastapi import APIRouter, HTTPException,Depends
from core.database import users_collection
from models.personal_info_model import PersonalInfoRequest
from datetime import datetime
from bson import ObjectId
from login.token_utils import *

router = APIRouter(prefix="/user", tags=["User"])


USER_PROJECTION = {
    "password": 0,
    "created_at": 0,
    "updated_at": 0
}

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get user info 
@router.get("/{user_id}",dependencies=[Depends(check_token)])
async def get_personal_info(user_id: str):
    try:
        oid = ObjectId(user_id)   # ensure valid ObjectId 
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await users_collection.find_one({"_id": oid},USER_PROJECTION)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])

    return user

# Update user info
@router.put("/{user_id}",dependencies=[Depends(check_token)])
async def update_personal_info(user_id: str, info: PersonalInfoRequest):
    # Ensure valid ObjectId
    try:
        oid = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Prepare update data
    update_data = {k: v for k, v in info.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_data["updated_at"] = now_str()

    result = await users_collection.update_one(
        {"_id": oid},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Personal information updated successfully"}

