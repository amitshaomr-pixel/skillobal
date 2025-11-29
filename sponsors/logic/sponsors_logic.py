from database.database import sponsors_collection


async def fetch_all_sponsors():
    """
    Fetch all sponsors.
    Returns => (sponsor_list, error)
    """

    sponsors = []

    async for sponsor in sponsors_collection.find({}):
        sponsor["id"] = str(sponsor.pop("_id"))  # Convert ObjectId → string
        sponsors.append(sponsor)

    if not sponsors:
        return None, "not_found"

    return sponsors, None
