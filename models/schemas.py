from pydantic import BaseModel, EmailStr , Field, HttpUrl

class OTPRequest(BaseModel):
    login_key: str

class VerifyRequest(BaseModel):
    login_key: str
    otp: str

class UserData(BaseModel):
    email: EmailStr
    name: str

    
class TokenRequest(BaseModel):
    id_token: str
