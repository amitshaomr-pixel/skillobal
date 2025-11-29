from fastapi import APIRouter, Depends
from middleware.token_verification import check_token
from users.logic.view_profile_logic import get_user_profile
from middleware.exceptions import CustomError   # ✅

router = APIRouter(tags=["Profile"])


@router.get("/profile", dependencies=[Depends(check_token)])
async def view_profile(user=Depends(check_token)):
    try:
        user_id = user["user_id"]
        profile = await get_user_profile(user_id)
        return profile

    except CustomError:
        raise
    except Exception as e:
        raise CustomError(f"Internal server error: {str(e)}", 500)
