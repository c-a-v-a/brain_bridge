"""Models for JWT tokens."""

from pydantic import BaseModel


class TokenPair(BaseModel):
    """Model representing a pair of JWT tokens."""
    access_token: str
    refresh_token: str
