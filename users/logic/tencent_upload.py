import os
import uuid
import io
from fastapi import UploadFile
from PIL import Image
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.vod.v20180717.vod_client import VodClient
from tencentcloud.vod.v20180717 import models
from qcloud_cos import CosConfig, CosS3Client
from middleware.exceptions import CustomError


SECRET_ID  = os.getenv("SECRET_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
SUBAPPID   = int(os.getenv("SUBAPPID"))
REGION     = os.getenv("REGION")  # Example: ap-mumbai


# ---------------------------------------------------------
# FUNCTION: Delete Tencent media by FileId
# ---------------------------------------------------------
def delete_tencent_media(file_id: str):
    try:
        if not file_id:
            return

        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        http_profile = HttpProfile(endpoint="vod.tencentcloudapi.com")
        client_profile = ClientProfile(httpProfile=http_profile)
        vod_client = VodClient(cred, REGION, client_profile)

        delete_req = models.DeleteMediaRequest()
        delete_req.SubAppId = SUBAPPID
        delete_req.FileId = file_id

        vod_client.DeleteMedia(delete_req)

    except Exception as e:
        print("⚠️ Tencent delete failed:", str(e))


# ---------------------------------------------------------
# FUNCTION: Upload profile image (RESIZED + VOD + COS)
# ---------------------------------------------------------
async def upload_profile_image(file: UploadFile) -> dict:
    # ---------------- Validate File Type ----------------
    ext = file.filename.split(".")[-1].lower()
    allowed = ["jpg", "jpeg", "png", "webp"]

    if ext not in allowed:
        raise CustomError("Only JPG, JPEG, PNG, WEBP allowed", 400)

    # ---------------- Validate File Size ----------------
    body = await file.read()
    if len(body) > 2 * 1024 * 1024:
        raise CustomError("Max size 2MB", 400)

    try:
        # ---------------- Step 1: ApplyUpload (VOD) ----------------
        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        http_profile = HttpProfile(endpoint="vod.tencentcloudapi.com")
        client_profile = ClientProfile(httpProfile=http_profile)
        vod_client = VodClient(cred, REGION, client_profile)

        apply_req = models.ApplyUploadRequest()
        apply_req.SubAppId = SUBAPPID
        apply_req.MediaType = "jpg"   # Always upload as JPEG
        apply_req.MediaName = f"profile_{uuid.uuid4()}.jpg"

        apply_resp = vod_client.ApplyUpload(apply_req)

        # COS temporary keys
        temp_secret_id  = apply_resp.TempCertificate.SecretId
        temp_secret_key = apply_resp.TempCertificate.SecretKey
        temp_token      = apply_resp.TempCertificate.Token
        bucket          = apply_resp.StorageBucket
        region          = apply_resp.StorageRegion
        media_path      = apply_resp.MediaStoragePath.lstrip("/")

        # ---------------- Step 2: Upload to COS ----------------
        cos_config = CosConfig(
            Region=region,
            SecretId=temp_secret_id,
            SecretKey=temp_secret_key,
            Token=temp_token
        )
        cos_client = CosS3Client(cos_config)

        cos_client.put_object(
            Bucket=bucket,
            Body=body,
            Key=media_path,
            StorageClass="STANDARD",
            ContentType="image/jpeg"
        )

        # ---------------- Step 3: CommitUpload ----------------
        commit_req = models.CommitUploadRequest()
        commit_req.SubAppId = SUBAPPID
        commit_req.VodSessionKey = apply_resp.VodSessionKey

        commit_resp = vod_client.CommitUpload(commit_req)

        # ---------------- Final URL + FileId ----------------
        final_url = commit_resp.MediaUrl
        final_file_id = commit_resp.FileId

        return {
            "ImageUrl": final_url,
            "FileId": final_file_id
        }

    except Exception as e:
        raise CustomError(f"Tencent upload failed: {str(e)}", 500)