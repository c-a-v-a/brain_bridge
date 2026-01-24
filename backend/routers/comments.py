"""FastAPI router for comments."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from crud.comments import get_comments, create_comment, delete_comment
from models.comment import Comment, CommentCreate, CommentFilter
from internals.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/",
    response_description="Create a new comment",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    comment: CommentCreate,
    current_user=Depends(get_current_user),
) -> Comment:
    """Create a new comment.

    The comment is automatically associated with the currently
    authenticated user.

    Raises:
        HTTPException: If the user is not authenticated.

    Returns:
        Comment: The newly created comment.
    """
    user_id = str(current_user.id)
    username = str(current_user.username)

    comment = await create_comment(user_id, username, comment)
    return comment


@router.get(
    "/{idea_id}",
    response_description="List all comments for a given idea",
    response_model=List[Comment],
)
async def list_comments_for_idea(
    idea_id: str,
) -> List[Comment]:
    """Retrieve all comments for a specific idea.

    Args:
        idea_id (str): ID of the idea.

    Returns:
        List[Comment]: List of comments associated with the idea.
    """
    comments = await get_comments(CommentFilter(idea_id=idea_id))
    return comments


@router.delete(
    "/{comment_id}",
    response_description="Delete a comment owned by the current user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    comment_id: str,
    current_user=Depends(get_current_user),
) -> None:
    """Delete a comment.

    Only the owner of the comment is allowed to delete it.

    Raises:
        HTTPException: If the comment does not exist or
        the current user is not the owner.

    Returns:
        None
    """
    user_id = str(current_user.id)

    deleted = await delete_comment(comment_id=comment_id, user_id=user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or not owned by current user",
        )

    return None


@router.post(
    "/{comment_id}/replies",
    response_description="Add a reply to an existing comment",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
async def add_reply_to_comment(
    comment_id: str,
    payload: Comment,
    current_user=Depends(get_current_user),
) -> Comment:
    """Add a reply to an existing comment.

    The reply is authored by the currently authenticated user
    and appended to the target comment.

    Raises:
        HTTPException: If the comment does not exist.

    Returns:
        Comment: The updated comment with the new reply added.
    """
    user_id = str(current_user.id)

    updated_comment = await comment_crud.add_reply(
        comment_id=comment_id,
        user_id=user_id,
        content=payload.content,
    )

    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return updated_comment
