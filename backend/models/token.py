"""Models for JWT tokens."""

from .base import CamelModel


class TokenPair(BaseModel):
    """Model representing a pair of JWT tokens."""
    access_token: str
    refresh_token: str
