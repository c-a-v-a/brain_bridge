"""Module providing CRUD functionality for working with users collection."""

from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.user import User, UserGet, UserUpdate, UserLogin

client = MongoDBConnector()
db = client.get_db()
users = db["users"]


async def create_user(user: User) -> UserGet:
    """Creates a new user and insetrs it into collection."""
    from internals.auth import get_password_hash

    new_user = user.model_dump(by_alias=True, exclude=["id"])
    new_user["password"] = get_password_hash(new_user["password"])

    result = await users.insert_one(new_user)
    new_user = await users.find_one({"_id": result.inserted_id})
    
    return UserGet.model_validate(new_user)


async def get_user(id: str) -> Optional[UserGet]:
    """Retrieves user with given id from the collection."""
    if not ObjectId.is_valid(id):
        return None

    user = await users.find_one({"_id": ObjectId(id)})

    if user:
        return UserGet.model_validate(user)

    return None


async def get_user_by_username(username: str) -> Optional[UserGet]:
    """Retrieves user with given username from the collection."""
    user = await users.find_one({"username": username})

    if user:
        return UserGet.model_validate(user)

    return None


async def get_user_by_email(email: str) -> Optional[UserGet]:
    """ 
    Retrieves user with given email from the collection.
    Used mostly for token validation.
    """
    user = await users.find_one({"email": email})

    if user:
        return UserGet.model_validate(user)

    return None


async def get_all_users() -> List[UserGet]:
    """Retrieves all users from the collection."""
    all_users = []

    async for user in users.find():
        all_users.append(UserGet.model_validate(user))

    return all_users


async def update_user(id: str, user: UserUpdate) -> Optional[UserGet]:
    """Updates the user with given id in the collection."""
    from internals.auth import get_password_hash

    if not ObjectId.is_valid(id):
        return None

    data = user.model_dump(by_alias=True, exclude_unset=True)

    if "password" in data:
        data["password"] = get_password_hash(data["password"])

    result = await users.update_one({"_id": ObjectId(id)}, {"$set": data})

    if result.modified_count == 1:
        updated = await users.find_one({"_id": ObjectId(id)})

        return UserGet.model_validate(updated)

    return None


async def delete_user(id: str) -> bool:
    """Deletes the user with given id from the collection."""
    if not ObjectId.is_valid(id):
        return False

    result = await users.delete_one({"_id": ObjectId(id)})

    return result.deleted_count == 1
