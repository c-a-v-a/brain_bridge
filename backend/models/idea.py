from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]


class Idea(BaseModel):
    """Full model representing an Idea document stored in MongoDB."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=1, max_length=200)
    user_id: PyObjectId
    desc: str = Field(..., min_length=1)
    long_desc: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaCreate(BaseModel):
    """Model for creating a new idea.

    This model includes only the fields required when a new idea
    is submitted by a user.
    """
    title: str = Field(..., min_length=1, max_length=200)
    user_id: PyObjectId
    desc: str = Field(..., min_length=1)
    long_desc: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaGet(BaseModel):  
    """Model returned in API responses.

    This model hides internal MongoDB representation details
    and exposes clean, client-side data. without long_desc
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    desc: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaFull(BaseModel):
    """Model returned in API responses.

    This model hides internal MongoDB representation details
    and exposes clean, client-side data. with long_desc
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    desc: str
    long_desc: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaUpdate(BaseModel):
    """Model for updating an idea.

    All fields are optional; only the ones provided will be updated.
    """

    title: Optional[str] = None
    user_id: Optional[PyObjectId] = None
    desc: Optional[str] = None
    long_desc: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
