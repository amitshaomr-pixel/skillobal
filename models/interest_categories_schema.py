from pydantic import BaseModel, validator
from typing import List
from middleware.exceptions import CustomError

class InterestCategoryRequest(BaseModel):
    category_ids: List[str]

    @validator("category_ids")
    def validate_min_three(cls, v):
        if len(v) < 3:
            # CORRECT
            raise CustomError("You have to select at least 3 categories", 422)

        return v
