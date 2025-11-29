from database.database import instructor_collection


async def fetch_all_mentors():

    mentors = []

    async for mentor in instructor_collection.find({}):
        mentors.append({
            "id": str(mentor["_id"]),
            "name": mentor.get("name"),
            "role": mentor.get("role"),
            "experience": mentor.get("experience"),
            "image_url": mentor.get("image_url")
        })

    if not mentors:
        return None, "not_found"

    return mentors, None
    