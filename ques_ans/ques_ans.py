from fastapi import APIRouter, HTTPException, Depends
from core.database import faqs_collection
from login.token_utils import check_token

router = APIRouter(tags=["FAQs"])

@router.get("/faqs",dependencies=[Depends(check_token)])
async def get_faqs():
    """Fetch FAQ section data"""
    faqs = []
    async for faq in faqs_collection.find({}):
        faqs.append({
            "id": str(faq["_id"]),
            "question": faq.get("question"),
            "answer": faq.get("answer")
        })

    if not faqs:
        raise HTTPException(status_code=404, detail="No FAQs found")

    return {
        "title": "Frequently Asked Questions",
        "subtitle": "Find answers to common questions about our courses and platform",
        "data": faqs
    }
