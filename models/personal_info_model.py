from pydantic import BaseModel, validator
from typing import List, Optional
from middleware.exceptions import CustomError

class PersonalInfoRequest(BaseModel):
    name: Optional[str] = None
    mobile: Optional[int] = None  
    selected_categories: Optional[List[str]] = None
    gender: Optional[str] = None

    @validator("mobile")
    def check_mobile(cls, v):
        if v is not None and len(str(v)) != 10:
            raise CustomError("Mobile number must be 10 digits", 400)
        return v
