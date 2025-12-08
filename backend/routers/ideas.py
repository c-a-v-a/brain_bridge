"""FastAPI router for managing ideas: creation, retrieval, update, deletion,
liking, unliking, and user-specific idea queries.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

from crud.ideas import (
    create_idea,
    get_idea,
    get_all_ideas,
    get_all_ideas_full,
    get_ideas_by_user,
    get_ideas_by_user_full,
    update_idea,
    delete_idea,
    like_idea,
    unlike_idea,
    get_ideas_liked_by_user,
)
from models.idea import IdeaCreate, IdeaGet, IdeaUpdate, IdeaFull

router = APIRouter(prefix="/ideas", tags=["ideas"])


class LikeRequest(BaseModel):
    """Request model for like/unlike actions."""
    user_id: str


@router.post(
    "/",
    response_model=IdeaFull,
    status_code=status.HTTP_201_CREATED,
    response_description="The newly created idea."
)
async def create_idea_endpoint(idea: IdeaCreate) -> IdeaFull:
    """Create a new idea.

    Args:
        idea (IdeaCreate): The idea data to insert.

    Returns:
        IdeaFull: The newly created idea including owner and like info.
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
    "/full",
    response_model=list[IdeaFull],
    response_description="All ideas from the database."
)
async def list_ideas_full() -> List[IdeaFull]:
    """Return all ideas with full details.

    Returns:
        List[IdeaFull]: Detailed idea objects.
    """
    return await get_all_ideas_full()


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
    return await get_ideas_by_user(user_id)


@router.get(
    "/user/{user_id}/full",
    response_model=list[IdeaFull],
    response_description="All ideas that belong to the user."
)
async def list_full_ideas_for_user(user_id: str) -> List[IdeaFull]:
    """Return all ideas by a user with full details.

    Args:
        user_id (str): User identifier.

    Returns:
        List[IdeaFull]: Detailed ideas created by the user.
    """
    return await get_ideas_by_user_full(user_id)


@router.get(
    "/{idea_id}",
    response_model=IdeaGet,
    response_description="Idea with given id."
)
async def get_idea_endpoint(idea_id: str) -> IdeaGet:
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


@router.get(
    "/full/{idea_id}",
    response_model=IdeaFull,
    response_description="Idea with given id."
)
async def get_full_idea_endpoint(idea_id: str) -> IdeaFull:
    """Retrieve a full-detail idea by ID.

    Args:
        idea_id (str): Idea identifier.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        IdeaFull: Detailed idea.
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
    response_model=IdeaFull,
    response_description="Updated idea."
)
async def update_idea_endpoint(idea_id: str, idea: IdeaUpdate) -> IdeaFull:
    """Update an existing idea.

    Args:
        idea_id (str): Idea identifier.
        idea (IdeaUpdate): Fields to update.

    Raises:
        HTTPException: If the idea does not exist or cannot be updated.

    Returns:
        IdeaFull: Updated idea with full details.
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


@router.post(
    "/{idea_id}/like",
    response_model=IdeaFull,
    response_description="Liked idea."
)
async def like_idea_endpoint(idea_id: str, data: LikeRequest) -> IdeaFull:
    """Like an idea as a user.

    Args:
        idea_id (str): Idea identifier.
        data (LikeRequest): Contains the user_id.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        IdeaFull: Updated idea with new like included.
    """
    idea = await like_idea(idea_id, data.user_id)
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea


@router.post(
    "/{idea_id}/unlike",
    response_model=IdeaFull,
    response_description="Disliked idea."
)
async def unlike_idea_endpoint(idea_id: str, data: LikeRequest) -> IdeaFull:
    """Remove a like from an idea.

    Args:
        idea_id (str): Idea identifier.
        data (LikeRequest): Contains the user_id.

    Raises:
        HTTPException: If the idea does not exist.

    Returns:
        IdeaFull: Updated idea without the user's like.
    """
    idea = await unlike_idea(idea_id, data.user_id)
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
    return await get_ideas_liked_by_user(user_id)
