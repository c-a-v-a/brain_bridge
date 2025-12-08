from bson import ObjectId
from typing import List, Optional

from crud.mongodb_connector import MongoDBConnector
from models.idea import IdeaCreate, IdeaGet, IdeaFull, IdeaUpdate


client = MongoDBConnector()
db = client.get_db()
ideas_collection = db["ideas"]


async def create_idea(idea: IdeaCreate) -> IdeaFull:
    """Utwórz nową ideę i zwróć pełny model (IdeaFull)."""
    
    doc = idea.model_dump(by_alias=True, exclude_none=True)

    result = await ideas_collection.insert_one(doc)
    created = await ideas_collection.find_one({"_id": result.inserted_id})

    return IdeaFull.model_validate(created)


async def get_idea(idea_id: str) -> Optional[IdeaFull]:
    """Pobierz jedną ideę po ID (pełny model)."""
    if not ObjectId.is_valid(idea_id):
        return None

    idea = await ideas_collection.find_one({"_id": ObjectId(idea_id)})
    if not idea:
        return None

    return IdeaFull.model_validate(idea)

async def get_all_ideas() -> list[IdeaGet]:
    ideas: list[IdeaGet] = []
    cursor = ideas_collection.find({})
    async for doc in cursor:
        # zamiana ObjectId na string
        doc["_id"] = str(doc["_id"])

      
        if "description" not in doc and "desc" in doc:
            doc["description"] = doc["desc"]

        ideas.append(IdeaGet.model_validate(doc))
    return ideas

async def get_all_ideas_full() -> List[IdeaFull]:
    """Pobierz wszystkie idee (pełny model, z long_description)."""
    ideas: List[IdeaFull] = []

    async for doc in ideas_collection.find():
        ideas.append(IdeaFull.model_validate(doc))

    return ideas


async def get_ideas_by_user(user_id: str) -> List[IdeaGet]:
    """Pobierz wszystkie idee użytkownika (mały model)."""
    ideas: List[IdeaGet] = []

    async for doc in ideas_collection.find({"user_id": user_id}):
        ideas.append(IdeaGet.model_validate(doc))

    return ideas


async def get_ideas_by_user_full(user_id: str) -> List[IdeaFull]:
    """Pobierz wszystkie idee użytkownika (pełny model)."""
    ideas: List[IdeaFull] = []

    async for doc in ideas_collection.find({"user_id": user_id}):
        ideas.append(IdeaFull.model_validate(doc))

    return ideas


async def update_idea(idea_id: str, idea: IdeaUpdate) -> Optional[IdeaFull]:
    """Zaktualizuj ideę i zwróć pełny model (IdeaFull)."""
    if not ObjectId.is_valid(idea_id):
        return None

    data = idea.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)

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
    """Usuń ideę po ID. Zwraca True, jeśli coś usunięto."""
    if not ObjectId.is_valid(idea_id):
        return False

    result = await ideas_collection.delete_one({"_id": ObjectId(idea_id)})
    return result.deleted_count == 1

async def like_idea(idea_id: str, user_id: str) -> Optional[IdeaFull]:
    """Dodaj lajka (user_id) do idei. Zwraca pełny model po update."""
    if not ObjectId.is_valid(idea_id):
        return None

    # Jeśli w Mongo trzymasz user_id jako stringi – zostaw tak jak jest.
    # Jeśli jako ObjectId, to tu daj ObjectId(user_id)
    result = await ideas_collection.update_one(
        {"_id": ObjectId(idea_id)},
        {"$addToSet": {"likedByUser": user_id}},  # brak duplikatów
    )

    if result.matched_count == 0:
        return None

    updated = await ideas_collection.find_one({"_id": ObjectId(idea_id)})
    if not updated:
        return None

    return IdeaFull.model_validate(updated)

async def unlike_idea(idea_id: str, user_id: str) -> Optional[IdeaFull]:
    """Usuń lajka (user_id) z idei. Zwraca pełny model po update."""
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
    """Pobierz wszystkie idee, które dany user polubił (mały model)."""
    ideas: List[IdeaGet] = []

    async for doc in ideas_collection.find({"likedByUser": user_id}):
        ideas.append(IdeaGet.model_validate(doc))

    return ideas
