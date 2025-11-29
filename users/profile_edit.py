from fastapi import APIRouter, Depends
from users.logic.profile_edit_logic import update_user_profile
from models.personal_info_model import PersonalInfoRequest
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # ✅

router = APIRouter(tags=["Profile"])


@router.patch("/edit-profile", dependencies=[Depends(check_token)])
async def edit_user(update_data: PersonalInfoRequest, user=Depends(check_token)):
    """Route to update user profile."""
    try:
        user_id = user["user_id"]

        update_dict = update_data.model_dump(exclude_none=True)

        await update_user_profile(user_id, update_dict)

        return {"message": "User updated successfully"}

    except CustomError:
        raise
    except Exception as e:
        raise CustomError(f"Internal server error: {str(e)}", 500)
