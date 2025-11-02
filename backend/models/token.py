"""
Models for JWT tokens.
"""

from pydantic import BaseModel


class TokenPair(BaseModel):
    """ 
    Model containing the JWT token and the type of the token (access/refresh).
    """
    access_token: str
    refresh_token: str
