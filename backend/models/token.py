"""Models for JWT tokens."""

from pydantic import BaseModel


class TokenPair(BaseModel):
    """
    Model representing a pair of JWT tokens.

    Attributes:
        access_token (str): The access token used for authenticating API
        requests.
        refresh_token (str): The refresh token used to obtain new access tokens.
    """
    access_token: str
    refresh_token: str
