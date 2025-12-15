"""FastAPI router for comments."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from crud.comments import get_comments, create_comment, delete_comment
from models.comment import Comment, CommentFilter
from internals.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    comment: Comment,
    current_user=Depends(get_current_user),
):
    user_id = str(current_user.id)
    comment = await create_comment(user_id, comment)

    return comment


@router.get(
    "/{idea_id}",
    response_model=List[Comment],
)
async def list_comments_for_idea(
    idea_id: str,
):
    comments = await get_comments(CommentFilter(idea_id=idea_id))

    return comments


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    comment_id: str,
    current_user=Depends(get_current_user),
):
    user_id = str(current_user.id)

    deleted = await delete_comment(comment_id=comment_id, user_id=user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or not owned by current user",
        )

    return
