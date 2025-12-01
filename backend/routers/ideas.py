from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from crud.ideas import (
    create_idea,
    get_idea,
    get_all_ideas,
    get_all_ideas_full,
    get_ideas_by_user,
    get_ideas_by_user_full,
    update_idea,
    delete_idea,
    like_idea,             # <-- DODAJ
    unlike_idea,           # <-- DODAJ
    get_ideas_liked_by_user,  # <-- DODAJ jeśli zrobiłeś tę funkcję
)

from models.idea import IdeaCreate, IdeaGet, IdeaUpdate, IdeaFull

router = APIRouter(prefix="/ideas", tags=["ideas"])

class LikeRequest(BaseModel):
    user_id: str

@router.post("/", response_model=IdeaFull, status_code=status.HTTP_201_CREATED)
async def create_idea_endpoint(idea: IdeaCreate):
    """Utwórz ideę – zwraca pełny model (z long_desc)."""
    created = await create_idea(idea)
    return created


@router.get("/", response_model=list[IdeaGet])
async def list_ideas():
    """Lista wszystkich idei – mały model (bez long_desc)."""
    return await get_all_ideas()


@router.get("/full", response_model=list[IdeaFull])
async def list_ideas_full():
    """Lista wszystkich idei – pełny model (z long_desc)."""
    return await get_all_ideas_full()


@router.get("/user/{user_id}", response_model=list[IdeaGet])
async def list_ideas_for_user(user_id: str):
    """Lista idei użytkownika – mały model."""
    return await get_ideas_by_user(user_id)


@router.get("/user/{user_id}/full", response_model=list[IdeaFull])
async def list_full_ideas_for_user(user_id: str):
    """Lista idei użytkownika – pełny model."""
    return await get_ideas_by_user_full(user_id)


@router.get("/{idea_id}", response_model=IdeaGet)
async def get_idea_endpoint(idea_id: str):
    """Pojedyncza idea – mały model (bez long_desc)."""
    idea = await get_idea(idea_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea


@router.get("/full/{idea_id}", response_model=IdeaFull)
async def get_full_idea_endpoint(idea_id: str):
    """Pojedyncza idea – pełny model (z long_desc)."""
    idea = await get_idea(idea_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea


@router.put("/{idea_id}", response_model=IdeaFull)
async def update_idea_endpoint(idea_id: str, idea: IdeaUpdate):
    """Update idei – zwraca pełny model (z long_desc)."""
    updated = await update_idea(idea_id, idea)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found or not updated",
        )
    return updated


@router.delete("/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea_endpoint(idea_id: str):
    """Usuń ideę."""
    deleted = await delete_idea(idea_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return None
@router.post("/{idea_id}/like", response_model=IdeaFull)
async def like_idea_endpoint(idea_id: str, data: LikeRequest):
    idea = await like_idea(idea_id, data.user_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea
@router.post("/{idea_id}/unlike", response_model=IdeaFull)
async def unlike_idea_endpoint(idea_id: str, data: LikeRequest):
    idea = await unlike_idea(idea_id, data.user_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea
@router.get("/liked/{user_id}", response_model=list[IdeaGet])
async def list_ideas_liked_by_user(user_id: str):
    """Lista idei polubionych przez użytkownika."""
    return await get_ideas_liked_by_user(user_id)
