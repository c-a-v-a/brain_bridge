# routers/comments.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from crud.mongodb_connector import MongoDBConnector
from crud.comments import CommentCRUD
from models.comment import CommentCreate, CommentInDB
from routers.auth import get_current_user  # dopasuj import do swojego projektu

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

# prosta inicjalizacja – jeśli masz gdzieś globalne get_db, możesz to przerobić
db = MongoDBConnector()
comment_crud = CommentCRUD(db)


@router.post(
    "",
    response_model=CommentInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    payload: CommentCreate,
    current_user=Depends(get_current_user),
):
    """
    POST /api/comments
    Tworzenie nowego komentarza pod ideą.
    """
   
    user_id = str(current_user.id)
    comment = await comment_crud.create_comment(user_id=user_id, data=payload)
    return comment


@router.get(
    "/{idea_id}",
    response_model=List[CommentInDB],
)
async def list_comments_for_idea(
    idea_id: str,
    current_user=Depends(get_current_user),  # jeśli chcesz publicznie, możesz to usunąć
):
    """
    GET /api/comments/{idea_id}
    Lista komentarzy dla konkretnej idei.
    """
    comments = await comment_crud.get_comments_for_idea(idea_id=idea_id)
    return comments


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: str,
    current_user=Depends(get_current_user),
):
    """
    DELETE /api/comments/{comment_id}
    Usuwanie komentarza należącego do zalogowanego użytkownika.
    """
    user_id = str(current_user.id)

    deleted = await comment_crud.delete_comment(comment_id=comment_id, user_id=user_id)
    if not deleted:
        # celowo nie rozróżniam 403/404, żeby nie ujawniać, że komentarz istnieje
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or not owned by current user",
        )
    # 204 – bez body
    return
