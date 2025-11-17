from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.idea import Idea, IdeaCreate, IdeaGet, IdeaUpdate

client = MongoDBConnector()
db = client.get_db()
ideas = db["ideas"]


async def create_idea(idea: IdeaCreate) -> IdeaGet:
    """Create a new idea.

    Args:
        idea (IdeaCreate): Data for creating a new idea.

    Returns:
        IdeaGet: The newly created idea with the database-assigned ID.
    """
    new_idea = idea.model_dump(by_alias=True, exclude=["id"])
    result = await ideas.insert_one(new_idea)
    created = await ideas.find_one({"_id": result.inserted_id})
    return IdeaGet.model_validate(created)


async def get_idea(idea_id: str) -> Optional[IdeaGet]:
    """Retrieve an idea by its ID.

    Args:
        idea_id (str): MongoDB ObjectId of the idea.

    Returns:
        Optional[IdeaGet]: The idea if found, otherwise None.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    idea = await ideas.find_one({"_id": ObjectId(idea_id)})
    if idea:
        return IdeaGet.model_validate(idea)

    return None


async def get_all_ideas() -> List[IdeaGet]:
    """Retrieve all ideas in the collection.

    Returns:
        List[IdeaGet]: A list of all ideas.
    """
    all_ideas: List[IdeaGet] = []

    async for idea in ideas.find():
        all_ideas.append(IdeaGet.model_validate(idea))

    return all_ideas


async def get_ideas_by_user(user_id: str) -> List[IdeaGet]:
    """Retrieve all ideas belonging to a specific user.

    Args:
        user_id (str): MongoDB ObjectId of the user.

    Returns:
        List[IdeaGet]: List of ideas matching the given user ID.
    """
    all_ideas: List[IdeaGet] = []

    async for idea in ideas.find({"user_id": user_id}):
        all_ideas.append(IdeaGet.model_validate(idea))

    return all_ideas


async def update_idea(idea_id: str, idea: IdeaUpdate) -> Optional[IdeaGet]:
    """Update an idea by its ID.

    Args:
        idea_id (str): MongoDB ObjectId of the idea to update.
        idea (IdeaUpdate): Fields to update.

    Returns:
        Optional[IdeaGet]: The updated idea if successful, otherwise None.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    data = idea.model_dump(by_alias=True, exclude_unset=True)
    result = await ideas.update_one({"_id": ObjectId(idea_id)}, {"$set": data})

    if result.modified_count == 1:
        updated = await ideas.find_one({"_id": ObjectId(idea_id)})
        return IdeaGet.model_validate(updated)

    return None


async def delete_idea(idea_id: str) -> bool:
    """Delete an idea by its ID.

    Args:
        idea_id (str): MongoDB ObjectId of the idea to delete.

    Returns:
        bool: True if the idea was deleted, otherwise False.
    """
    if not ObjectId.is_valid(idea_id):
        return False

    result = await ideas.delete_one({"_id": ObjectId(idea_id)})
    return result.deleted_count == 1
