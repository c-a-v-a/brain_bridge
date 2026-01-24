"""Module defining Pydantic models for Comment objects."""

from datetime import datetime
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List, Optional

from .base import CamelModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class Comment(CamelModel):
    """Base model for comment collection."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    username: str = Field(default="")
    content: str
    replies: List[str] = Field(default_factory=list)
    idea_id: Optional[PyObjectId] = Field(default=None)


class CommentCreate(CamelModel):
    """Model for creating comments."""
    user_id: Optional[PyObjectId] = Field(default=None)
    username: Optional[str] = Field(default=None)
    idea_id: PyObjectId = Field(default=None)
    content: str


class CommentUpdate(CamelModel):
    """Model for updating comment."""
    content: Optional[str] = None
    replies: Optional[List[str]] = None


class CommentFilter(CommentUpdate):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    idea_id: Optional[PyObjectId] = Field(default=None)
