from database.database import contact_collection

async def fetch_contact():

    contact = await contact_collection.find_one({})
    if not contact:
        return None

    contact["id"] = str(contact.pop("_id"))
    return contact
