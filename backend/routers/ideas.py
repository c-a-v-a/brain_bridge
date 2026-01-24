"""FastAPI router for managing ideas: creation, retrieval, update, deletion,
liking, unliking, and user-specific idea queries.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

from crud.ideas import (
    create_idea,
    delete_idea,
    get_idea,
    get_ideas,
    get_all_ideas,
    get_liked_ideas,
    like_idea,
    unlike_idea,
    update_idea
)
from internals.auth import get_current_user
from models.idea import Idea, IdeaCreate, IdeaFilter, IdeaGet, IdeaUpdate

router = APIRouter(prefix="/ideas", tags=["ideas"])


class LikeRequest(BaseModel):
    """Request model for like/unlike actions."""
    user_id: str


@router.post(
    "/",
    response_model=Idea,
    status_code=status.HTTP_201_CREATED,
    response_description="The newly created idea."
)
async def create_idea_endpoint(idea: IdeaCreate) -> Idea:
    """Create a new idea.

    Args:
        idea (IdeaCreate): The idea data to insert.

    Returns:
        Idea: The newly created idea including owner and like info.
    """
    created = await create_idea(idea)
    return created


@router.get(
    "/",
    response_model=list[IdeaGet],
    response_description="All ideas from the database."
)
async def list_ideas() -> List[IdeaGet]:
    """Return all ideas in a compact format.

    Returns:
        List[IdeaGet]: All stored ideas.
    """
    return await get_all_ideas()


@router.get(
    "/user/{user_id}",
    response_model=list[IdeaGet],
    response_description="All ideas that belong to the user."
)
async def list_ideas_for_user(user_id: str) -> List[IdeaGet]:
    """Return all ideas belonging to a specific user.

    Args:
        user_id (str): User identifier.

    Returns:
        List[IdeaGet]: Ideas created by the user.
    """
    ideas = await get_idea(IdeaFilter(user_id=user_id))

    return [IdeaGet.model_validate(idea.model_dump()) for idea in ideas]


@router.get(
    "/{idea_id}",
    response_model=Idea,
    response_description="Idea with given id."
)
async def get_idea_endpoint(idea_id: str) -> Idea:
    """Retrieve a single idea by ID.

    Args:
        idea_id (str): Idea identifier.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        IdeaGet: The matching idea.
    """
    idea = await get_idea(idea_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea


@router.put(
    "/{idea_id}",
    response_model=Idea,
    response_description="Updated idea."
)
async def update_idea_endpoint(idea_id: str, idea: IdeaUpdate) -> Idea:
    """Update an existing idea.

    Args:
        idea_id (str): Idea identifier.
        idea (IdeaUpdate): Fields to update.

    Raises:
        HTTPException: If the idea does not exist or cannot be updated.

    Returns:
        Idea: Updated idea with full details.
    """
    updated = await update_idea(idea_id, idea)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found or not updated",
        )

    return updated


@router.delete("/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea_endpoint(idea_id: str) -> None:
    """Delete an idea.

    Args:
        idea_id (str): Idea identifier.

    Raises:
        HTTPException: If the idea does not exist.
    """
    deleted = await delete_idea(idea_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

    return None


@router.put(
    "/{idea_id}/like",
    response_model=Idea,
    response_description="Liked idea."
)
async def like_idea_endpoint(idea_id: str, current_user=Depends(get_current_user)) -> Idea:
    """Like an idea as a user.

    Args:
        idea_id (str): Idea identifier.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        Idea: Updated idea with new like included.
    """
    idea = await like_idea(idea_id, current_user.id)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

    return idea


@router.put(
    "/{idea_id}/unlike",
    response_model=Idea,
    response_description="Disliked idea."
)
async def unlike_idea_endpoint(idea_id: str, current_user=Depends(get_current_user)) -> Idea:
    """Remove a like from an idea.

    Args:
        idea_id (str): Idea identifier.
        data (LikeRequest): Contains the user_id.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        Idea: Updated idea without the user's like.
    """
    idea = await unlike_idea(idea_id, current_user.id)

    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

    return idea


@router.get(
    "/liked/{user_id}",
    response_model=list[IdeaGet],
    response_description="Ideas liked by the user"
)
async def list_ideas_liked_by_user(user_id: str) -> List[IdeaGet]:
    """Return all ideas liked by a given user.

    Args:
        user_id (str): User identifier.

    Returns:
        List[IdeaGet]: Ideas the user has liked.
    """
    return await get_liked_ideas(user_id)
