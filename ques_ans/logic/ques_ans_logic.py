from database.database import faqs_collection


async def fetch_all_faqs():
    """
    Fetch all FAQs.
    Returns => (faq_list, error)
    """

    faqs = []

    async for faq in faqs_collection.find({}):
        faqs.append({
            "id": str(faq["_id"]),
            "question": faq.get("question"),
            "answer": faq.get("answer")
        })

    if not faqs:
        return None, "not_found"

    return faqs, None
