"""Module providing CRUD operations for the 'users' collection."""

from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.user import User, UserGet, UserCreate, UserUpdate

client = MongoDBConnector()
db = client.get_db()
users = db["users"]


async def create_user(user: UserCreate) -> UserGet:
    """Create a new user and insert it into the collection.

    Hashes the user's password before saving.

    Args:
        user (UserCreate): The user data to insert.

    Returns:
        UserGet: The newly created user with database-assigned ID.
    """
    from internals.auth import get_password_hash

    new_user = user.model_dump(by_alias=True, exclude=["id"])
    new_user["password"] = get_password_hash(new_user["password"])

    result = await users.insert_one(new_user)
    new_user = await users.find_one({"_id": result.inserted_id})

    return UserGet.model_validate(new_user)


async def get_user(user_id: str) -> Optional[UserGet]:
    """Retrieve a user by their ID.

    Args:
        user_id (str): The MongoDB ObjectId of the user.

    Returns:
        Optional[UserGet]: The user if found, otherwise None.
    """
    if not ObjectId.is_valid(user_id):
        return None

    user = await users.find_one({"_id": ObjectId(user_id)})

    if user:
        return UserGet.model_validate(user)

    return None


async def get_user_by_username(username: str) -> Optional[UserGet]:
    """Retrieve a user by their username.

    Args:
        username (str): The username to search for.

    Returns:
        Optional[UserGet]: The user if found, otherwise None.
    """
    user = await users.find_one({"username": username})

    if user:
        return UserGet.model_validate(user)

    return None


async def get_user_by_email(email: str) -> Optional[User]:
    """Retrieve a user by their email.

    Typically used for authentication and token validation.

    Args:
        email (str): The email address to search for.

    Returns:
        Optional[UserGet]: The user if found, otherwise None.
    """
    user = await users.find_one({"email": email})

    if user:
        return User.model_validate(user)

    return None


async def get_all_users() -> List[UserGet]:
    """Retrieve all users from the collection.

    Returns:
        List[UserGet]: A list of all users.
    """
    all_users = []

    async for user in users.find():
        all_users.append(UserGet.model_validate(user))

    return all_users


async def update_user(user_id: str, user: UserUpdate) -> Optional[UserGet]:
    """Update a user by their ID.

    Hashes the password if it is being updated.

    Args:
        user_id (str): The MongoDB ObjectId of the user to update.
        user (UserUpdate): The fields to update.

    Returns:
        Optional[UserGet]: The updated user if successful, otherwise None.
    """
    from internals.auth import get_password_hash

    if not ObjectId.is_valid(user_id):
        return None

    data = user.model_dump(by_alias=True, exclude_unset=True)

    if "password" in data:
        data["password"] = get_password_hash(data["password"])

    result = await users.update_one({"_id": ObjectId(user_id)}, {"$set": data})

    if result.modified_count == 1:
        updated = await users.find_one({"_id": ObjectId(user_id)})

        return UserGet.model_validate(updated)

    return None


async def delete_user(user_id: str) -> bool:
    """Delete a user by their ID.

    Args:
        user_id (str): The MongoDB ObjectId of the user to delete.

    Returns:
        bool: True if a user was deleted, False otherwise.
    """
    if not ObjectId.is_valid(user_id):
        return False

    result = await users.delete_one({"_id": ObjectId(user_id)})

    return result.deleted_count == 1
