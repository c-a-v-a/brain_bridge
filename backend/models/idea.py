"""Module defining Pydantic models for Ideas objects."""

from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List, Optional

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
    images: Optional[List[str]] = Field(default_factory=list)
    liked_by_user: List[PyObjectId] = Field(
        default_factory=list,
        alias="likedByUser"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaCreate(BaseModel):
    """Model for creating a new idea."""
    title: str = Field(..., min_length=1, max_length=200)
    user_id: PyObjectId
    description: str = Field(..., min_length=1)
    long_description: Optional[str] = None
    links: List[Link]
    wanted_contributors: str
    liked_by_user: List[PyObjectId] = Field(
        default_factory=list,
        alias="likedByUser"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaGet(BaseModel):
    """Model returned in API responses (bez long_description)."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    description: str
    liked_by_user: List[PyObjectId] = Field(
        default_factory=list,
        alias="likedByUser"
    )

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
    links: Optional[List[Link]] = None
    wanted_contributors: Optional[str] = None
    images: Optional[List[str]] = None
    liked_by_user: Optional[List[PyObjectId]] = Field(
        default=None,
        alias="likedByUser"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdeaFilter(IdeaUpdate):
    """Model returned in API responses (z long_description)."""
    id: Optional[str] = Field(alias="_id", default=None)

