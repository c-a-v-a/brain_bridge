"""Module that provides the CRUD functionality for 'ideas' collection."""

from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.idea import IdeaCreate, IdeaGet, IdeaFull, IdeaUpdate


client = MongoDBConnector()
db = client.get_db()
ideas_collection = db["ideas"]


async def create_idea(idea: IdeaCreate) -> IdeaFull:
    """Saves the new idea to the database.
    
    Args:
        idea (IdeaCreate): The idea that should be added to the database.

    Returns:
        IdeaFull: The newly added idea.
    """

    doc = idea.model_dump(by_alias=True, exclude_none=True)

    result = await ideas_collection.insert_one(doc)
    created = await ideas_collection.find_one({"_id": result.inserted_id})

    return IdeaFull.model_validate(created)


async def get_idea(idea_id: str) -> Optional[IdeaFull]:
    """Get one idea with given id.
    
    Args:
        idea_id (str): The id of idea that will be returned.

    Returns:
        IdeaFull: The idea that was found in the database.
        None: If no ideas were found.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    idea = await ideas_collection.find_one({"_id": ObjectId(idea_id)})
    if not idea:
        return None

    return IdeaFull.model_validate(idea)


async def get_all_ideas() -> List[IdeaGet]:
    """Get all ideas from the database.
    
    Returns:
        List[IdeaGet]: All the ideas from the database.
    """
    ideas: List[IdeaGet] = []

    async for doc in ideas_collection.find():
        ideas.append(IdeaGet.model_validate(doc))

    return ideas


async def get_all_ideas_full() -> List[IdeaFull]:
    """Get all ideas from the database.
    
    Returns:
        List[IdeaFull]: All the ideas from the database.
    """
    ideas: List[IdeaFull] = []

    async for doc in ideas_collection.find():
        ideas.append(IdeaFull.model_validate(doc))

    return ideas


async def get_ideas_by_user(user_id: str) -> List[IdeaGet]:
    """Get all ideas created by a given user.
    
    Args:
        user_id (str): Id of the user that created the ideas.

    Returns:
        List[IdeaGet]: All ideas that belong to the user.
    """
    ideas: List[IdeaGet] = []

    async for doc in ideas_collection.find({"user_id": user_id}):
        ideas.append(IdeaGet.model_validate(doc))

    return ideas


async def get_ideas_by_user_full(user_id: str) -> List[IdeaFull]:
    """Get all ideas created by a given user.
    
    Args:
        user_id (str): Id of the user that created the ideas.

    Returns:
        List[IdeaFull]: All ideas that belong to the user.
    """
    ideas: List[IdeaFull] = []

    async for doc in ideas_collection.find({"user_id": user_id}):
        ideas.append(IdeaFull.model_validate(doc))

    return ideas


async def update_idea(idea_id: str, idea: IdeaUpdate) -> Optional[IdeaFull]:
    """Update idea with given id.
    
    Args:
        idea_id (str): The id of the idea that needs to be updated.
        idea (IdeaUpdate): The model with fields that will be updated.

    Returns:
        IdeaFull: The idea that was updated, with updated fields.
        None: If the idea wasn't updated.
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

    result = await ideas_collection.update_one(
        {"_id": ObjectId(idea_id)},
        {"$set": data},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas_collection.find_one({"_id": ObjectId(idea_id)})

    if not updated:
        return None

    return IdeaFull.model_validate(updated)


async def delete_idea(idea_id: str) -> bool:
    """Deletes the idea with given id.
    
    Args:
        idea_id (str): The id of the idea that will be deleted.

    Returns:
        bool: True if the idea was deleted. False otherwise.
    """
    if not ObjectId.is_valid(idea_id):
        return False

    result = await ideas_collection.delete_one({"_id": ObjectId(idea_id)})
    return result.deleted_count == 1


async def like_idea(idea_id: str, user_id: str) -> Optional[IdeaFull]:
    """Add the user with given id, to the likedByUser field.
    
    Args:
        idea_id (str): The id of the idea.
        user_id (str): The id of the user that likes the idea.

    Returns:
        IdeaFull: The idea that was liked by the user.
        None: If the idea was not found.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    result = await ideas_collection.update_one(
        {"_id": ObjectId(idea_id)},
        {"$addToSet": {"likedByUser": user_id}},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas_collection.find_one({"_id": ObjectId(idea_id)})

    if not updated:
        return None

    return IdeaFull.model_validate(updated)


async def unlike_idea(idea_id: str, user_id: str) -> Optional[IdeaFull]:
    """Remove the user with given id, to the likedByUser field.
    
    Args:
        idea_id (str): The id of the idea.
        user_id (str): The id of the user that disliked the idea.

    Returns:
        IdeaFull: The idea that was disliked by the user.
        None: If the idea was not found.
    """
    if not ObjectId.is_valid(idea_id):
        return None

    result = await ideas_collection.update_one(
        {"_id": ObjectId(idea_id)},
        {"$pull": {"likedByUser": user_id}},
    )

    if result.matched_count == 0:
        return None

    updated = await ideas_collection.find_one({"_id": ObjectId(idea_id)})
    if not updated:
        return None

    return IdeaFull.model_validate(updated)


async def get_ideas_liked_by_user(user_id: str) -> List[IdeaGet]:
    """Get all ideas the were liked by the user with given id.
    
    Args:
        user_id (str): Id of the user.

    Returns:
        List[IdeaGet]: All the ideas liked by user.
    """
    ideas: List[IdeaGet] = []

    async for doc in ideas_collection.find({"likedByUser": user_id}):
        ideas.append(IdeaGet.model_validate(doc))

    return ideas
