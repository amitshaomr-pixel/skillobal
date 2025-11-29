from fastapi import APIRouter, Depends, File, UploadFile
from users.logic.tencent_upload import upload_profile_image, delete_tencent_media
from bson import ObjectId
from middleware.token_verification import check_token
from database.database import users_collection
from middleware.exceptions import CustomError   # ✅

router = APIRouter(tags=["Profile"])


@router.patch("/update-profile-image")
async def update_profile_image(
    file: UploadFile = File(...),
    user=Depends(check_token)
):
    try:
        user_id = user["user_id"]

        existing_user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise CustomError("User not found", 404)

        old_file_id = existing_user.get("tencent_file_id")

        upload_data = await upload_profile_image(file)
        image_url = upload_data["ImageUrl"]
        file_id = upload_data["FileId"]

        if old_file_id:
            delete_tencent_media(old_file_id)

        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "profile_image": image_url,
                    "tencent_file_id": file_id
                }
            }
        )

        if result.matched_count == 0:
            raise CustomError("User not found", 404)

        return {
            "status": True,
            "message": "Profile image updated successfully",
            "image_url": image_url,
            # "fileId": file_id
        }

    except CustomError:
        raise
    except Exception as e:
        raise CustomError(f"Internal server error: {str(e)}", 500)
