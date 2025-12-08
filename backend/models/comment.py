
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class CommentBase(BaseModel):
    idea_id: str = Field(..., description="ID powiązanego pomysłu")
    content: str = Field(..., min_length=1, max_length=2000)


class CommentCreate(CommentBase):
    """Payload do tworzenia komentarza z requestu."""
    pass


class CommentInDB(CommentBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime

    class Config:
        populate_by_name = True  # pozwala zwracać `id` zamiast `_id`
