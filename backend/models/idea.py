from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]


class Link(BaseModel):
    url: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class Idea(BaseModel):
    """Full model representing an Idea document stored in MongoDB."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=1, max_length=200)
    user_id: PyObjectId
    description: str = Field(..., min_length=1)
    long_description: Optional[str] = None
    links: List[Link]
    wanted_contributors: str

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
    description: str = Field(..., min_length=1)
    long_description: Optional[str] = None
    links: List[Link]
    wanted_contributors: str


    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaGet(BaseModel):  
    """Model returned in API responses.

    This model hides internal MongoDB representation details
    and exposes clean, client-side data. without long_description
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    description: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaFull(BaseModel):
    """Model returned in API responses.

    This model hides internal MongoDB representation details
    and exposes clean, client-side data. with long_description
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    description: str
    long_description: Optional[str] = None
    links: List[Link]
    wanted_contributors: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaUpdate(BaseModel):
    """Model for updating an idea.

    All fields are optional; only the ones provided will be updated.
    """
    title: Optional[str] = None
    user_id: Optional[PyObjectId] = None
    description: Optional[str] = None
    long_description: Optional[str] = None
    links: List[Link]
    wanted_contributors: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
