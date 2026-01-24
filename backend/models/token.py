"""Models for JWT tokens."""

from .base import CamelModel


class TokenPair(CamelModel):
    """Model representing a pair of JWT tokens."""
    access_token: str
    refresh_token: str
