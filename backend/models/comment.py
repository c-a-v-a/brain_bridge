"""Module defining Pydantic models for Comment objects."""

from datetime import datetime
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]


class Comment(BaseModel):
    """Base model for comment collection."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    content: str
    created_at: datetime
    replies: List[str] = []

    class Config:
        populate_by_name = True


class CommentUpdate(BaseModel):
    """Model for updating comment."""
    content: Optional[str] = None
    replies: Optional[List[str]] = []

    class Config:
        populate_by_name = True


class CommentFilter(CommentUpdate):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
