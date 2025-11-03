"""Module that handles models for User objects."""

from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    """
    Base model for User objects. This model is also used to create a new user.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserGet(BaseModel):
    """Model for retrieving User data."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    """
    Model for update operations on user. Id should be passed from route and not
    included in the model.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
