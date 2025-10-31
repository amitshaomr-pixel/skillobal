from pydantic import BaseModel
from typing import Optional

class PersonalInfoRequest(BaseModel):
    name: Optional[str] = None
    phone_number: str = None
    photo: Optional[str] = None 
    gender : Optional[str]  
