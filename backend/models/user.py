"""Module defining Pydantic models for User objects and authentication."""

from pydantic import BaseModel, BeforeValidator, EmailStr, Field
from typing import Annotated, Optional

from .base import CamelModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(CamelModel):
    """Base model for a User object, including all attributes stored in the
    database.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)


class UserCreate(CamelModel):
    """Model for creating new users."""
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)


class UserGet(CamelModel):
    """Model for responses. Sends user data without the password."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)


class UserUpdate(CamelModel):
    """Model for updating user information.

    Fields are all optional; the user ID should be provided separately
    (e.g., via route parameters).
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    is_admin: Optional[bool] = None


class UserLogin(CamelModel):
    """Model for user login credentials with email and password."""
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserFilter(CamelModel):
    """Model for searchin users in the database."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
