"""Module that provides the CRUD functionality for 'ideas' collection."""

from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.idea import Idea, IdeaCreate, IdeaFilter, IdeaGet, IdeaUpdate


client = MongoDBConnector()
db = client.get_db()
ideas = db["ideas"]


# Create
async def create_idea(idea: IdeaCreate) -> Idea:
    """Saves the new idea to the database.
    
    Args:
        idea (IdeaCreate): The idea that should be added to the database.

    Returns:
        Idea: The newly added idea.
    """
    doc = idea.model_dump(by_alias=True, exclude_none=True)

    result = await ideas.insert_one(doc)
    created = await ideas.find_one({"_id": result.inserted_id})

    return Idea.model_validate(created)


# Read
async def get_idea(idea_id: str) -> Optional[Idea]:
    """Get one idea with given id.
    
    Args:
        idea_id (str): The id of idea that will be returned.

    Returns:
        Idea: The idea that was found in the database.
        None: If no ideas were found.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    idea = await ideas.find_one({"_id": ObjectId(idea_id)})
    if not idea:
        return None

    return Idea.model_validate(idea)


async def get_ideas(filters: IdeaFilter) -> List[Idea]:
    """Get ideas that match the filter.
    
    Args:
        filter (IdeaFilter): Filters that are used when searching for the idea.

    Returns:
        List[Idea]: The ideas matching the filter.
    """
    query = filters.model_dump(exclude_none=True, by_alias=True)

    if not query:
        return None

    cursor = ideas.find(query)
    result = []

    async for doc in cursor:
        result.append(Idea.validate(doc))

    return result


async def get_all_ideas() -> List[IdeaGet]:
    """Get all ideas from the database.
    
    Returns:
        List[Idea]: All the ideas from the database.
    """
    result = []

    async for doc in ideas.find():
        result.append(IdeaGet.model_validate(doc))

    return result


# Update
async def update_idea(idea_id: str, idea: IdeaUpdate) -> Optional[Idea]:
    """Update idea with given id.
    
    Args:
        idea_id (str): The id of the idea that needs to be updated.
        idea (IdeaUpdate): The model with fields that will be updated.

    Returns:
        Optional[Idea]: The idea that was updated, with updated fields,
        None otherwise.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    data = idea.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude_none=True,
        exclude={"id"}
    )

    if not data:
        return None

    result = await ideas.update_one(
        {"_id": ObjectId(idea_id)},
        {"$set": data},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas.find_one({"_id": ObjectId(idea_id)})

    if not updated:
        return None

    return Idea.model_validate(updated)


async def like_idea(idea_id: str, user_id: str) -> Optional[Idea]:
    """Add the user with given id, to the likedByUser field.
    
    Args:
        idea_id (str): The id of the idea.
        user_id (str): The id of the user that likes the idea.

    Returns:
        Optional[Idea]: The idea that was liked by the user, None otherwise.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    result = await ideas.update_one(
        {"_id": ObjectId(idea_id)},
        {"$addToSet": {"likedByUser": user_id}},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas.find_one({"_id": ObjectId(idea_id)})

    if not updated:
        return None

    return Idea.model_validate(updated)


async def unlike_idea(idea_id: str, user_id: str) -> Optional[Idea]:
    """Remove the user with given id, to the likedByUser field.
    
    Args:
        idea_id (str): The id of the idea.
        user_id (str): The id of the user that disliked the idea.

    Returns:
        Optional[Idea]: The idea that was disliked by the user, None otherwise.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    result = await ideas.update_one(
        {"_id": ObjectId(idea_id)},
        {"$pull": {"likedByUser": user_id}},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas.find_one({"_id": ObjectId(idea_id)})
    if not updated:
        return None

    return Idea.model_validate(updated)


# Delete
async def delete_idea(idea_id: str) -> bool:
    """Deletes the idea with given id.
    
    Args:
        idea_id (str): The id of the idea that will be deleted.

    Returns:
        bool: True if the idea was deleted. False otherwise.
    """
    if not ObjectId.is_valid(idea_id):
        return False

    result = await ideas.delete_one({"_id": ObjectId(idea_id)})
    return result.deleted_count == 1
