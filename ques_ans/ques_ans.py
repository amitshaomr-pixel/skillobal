from fastapi import APIRouter, Depends
from ques_ans.logic.ques_ans_logic import fetch_all_faqs
from middleware.token_verification import check_token
from middleware.exceptions import CustomError   # ✅ use custom error

router = APIRouter(tags=["FAQs"])


@router.get("/faqs", dependencies=[Depends(check_token)])
async def get_faqs():
    """Fetch FAQ section data"""

    faqs, error = await fetch_all_faqs()

    if error == "not_found":
        raise CustomError("No FAQs found", 404)   # ✅ replaced HTTPException

    return {
        "title": "Frequently Asked Questions",
        "subtitle": "Find answers to common questions about our courses and platform",
        "data": faqs
    }
