"""
Module that handles models for User objects.
"""

# TODO: Connect with mongodb

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    """
    Base model for User objects. This model is also used to create a new user.
    """
    id: int = Field(...)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)
    surename: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserGet(BaseModel):
    """
    Model for retrieving User data.
    """
    id: int = Field(...)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    name: str = Field(..., min_length=1, max_length=100)
    surename: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """
    Model for update operations on user. Id should be passed from route and not
    included in the model.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surename: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        from_attributes = True
