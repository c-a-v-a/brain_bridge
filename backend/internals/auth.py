"""
Module responsible for handling user authentication and JWT tokens.
"""

import jwt
import os
from datetime import timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from typing import Optional

from crud.user import get_user_by_email
from models.user import UserGet, UserLogin
from settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
PASSWORD_HASH = PasswordHash.recommended()
settings = Settings()


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a new token and encodes information from the data argument
    into the tokens.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode token from token string to dict.
    """
    return jwt.decode(token, settings.SECRET_KEY,
                      algorithms=[settings.ALGORITHM])


def verify_password(plain: str, hashed: str) -> bool:
    """ Verify that the plain password matches it hasehd counterpart. """
    return PASSWORD_HASH.verify(plain, hashed)


def get_password_hash(plain: str) -> str:
    """ Get a hashed version of the password for storage purposes. """
    return PASSWORD_HASH.hash(plain)


def authenticate_user(user: UserLogin) -> Optional[UserGet]:
    """
    Try to match given user, with one of the database users and veirfy that
    given password is correct.
    """
    auth_user = get_user_by_email(user.email)
    
    if not user:
        return None
    
    if not verify_password(user.password, auth_user.password):
        return None

    return auth_user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserGet:
    """ Get current bearer of the token. Only works if the token is valid. """
    data = decode_token(token)

    if not data or data.get("type") != "access":
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token")
    
    email = data.get("sub")
    user = get_user_by_email(email)

    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found")

    return user
