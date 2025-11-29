from database.database import hero_collection


async def fetch_hero_section():

    hero = await hero_collection.find_one({})
    if not hero:
        return None, "not_found"

    hero["id"] = str(hero.pop("_id"))  # Convert ObjectId → string

    return hero, None
