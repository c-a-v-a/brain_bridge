from fastapi import APIRouter, HTTPException, status

from crud.ideas import (
    create_idea,
    get_idea,
    get_all_ideas,
    get_all_ideas_full,
    get_ideas_by_user,
    get_ideas_by_user_full,
    update_idea,
    delete_idea,
)

from models.idea import IdeaCreate, IdeaGet, IdeaUpdate, IdeaFull

router = APIRouter(prefix="/ideas", tags=["ideas"])


# ---------- CREATE ----------

@router.post("/", response_model=IdeaFull, status_code=status.HTTP_201_CREATED)
async def create_idea_endpoint(idea: IdeaCreate):
    """Utwórz ideę – zwraca pełny model (z long_desc)."""
    created = await create_idea(idea)
    return created


# ---------- LISTY GLOBALNE ----------

@router.get("/", response_model=list[IdeaGet])
async def list_ideas():
    """Lista wszystkich idei – mały model (bez long_desc)."""
    return await get_all_ideas()


@router.get("/full", response_model=list[IdeaFull])
async def list_ideas_full():
    """Lista wszystkich idei – pełny model (z long_desc)."""
    return await get_all_ideas_full()


# ---------- LISTY PER USER ----------

@router.get("/user/{user_id}", response_model=list[IdeaGet])
async def list_ideas_for_user(user_id: str):
    """Lista idei użytkownika – mały model."""
    return await get_ideas_by_user(user_id)


@router.get("/user/{user_id}/full", response_model=list[IdeaFull])
async def list_full_ideas_for_user(user_id: str):
    """Lista idei użytkownika – pełny model."""
    return await get_ideas_by_user_full(user_id)


# ---------- GET ONE ----------

@router.get("/{idea_id}", response_model=IdeaGet)
async def get_idea_endpoint(idea_id: str):
    """Pojedyncza idea – mały model (bez long_desc)."""
    idea = await get_idea(idea_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    # get_idea zwraca IdeaFull, ale response_model=IdeaGet przytnie pola
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


# ---------- UPDATE ----------

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


# ---------- DELETE ----------

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
