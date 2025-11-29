from database.database import testimonials_collection


async def fetch_all_testimonials():
    testimonials = []

    async for t in testimonials_collection.find({}):
        testimonials.append({
            "id": str(t["_id"]),
            "message": t.get("message"),
            "name": t.get("name"),
            "designation": t.get("designation"),
            "profile_image": t.get("profile_image")
        })

    return testimonials
