from fastapi import APIRouter, HTTPException, status

from crud.ideas import (
    create_idea,
    get_idea,
    get_all_ideas,
    get_ideas_by_user,
    update_idea,
    delete_idea,
)

from models.idea import IdeaCreate, IdeaGet, IdeaUpdate

router = APIRouter(prefix="/ideas", tags=["ideas"])


@router.post("/", response_model=IdeaGet, status_code=status.HTTP_201_CREATED)
async def create_idea_endpoint(idea: IdeaCreate):
    return await create_idea(idea)


@router.get("/", response_model=list[IdeaGet])
async def list_ideas():
    return await get_all_ideas()


@router.get("/user/{user_id}", response_model=list[IdeaGet])
async def list_ideas_for_user(user_id: str):
    return await get_ideas_by_user(user_id)


@router.get("/{idea_id}", response_model=IdeaGet)
async def get_idea_endpoint(idea_id: str):
    idea = await get_idea(idea_id)
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Idea not found")
    return idea


@router.put("/{idea_id}", response_model=IdeaGet)
async def update_idea_endpoint(idea_id: str, idea: IdeaUpdate):
    updated = await update_idea(idea_id, idea)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Idea not found or not updated")
    return updated


@router.delete("/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea_endpoint(idea_id: str):
    deleted = await delete_idea(idea_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Idea not found")
    return None
