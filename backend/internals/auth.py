"""Module responsible for handling user authentication and JWT tokens."""

import jwt
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pwdlib import PasswordHash
from typing import Optional

from crud.user import get_user_by_email
from models.user import UserGet, UserLogin, User
from settings import Settings

auth_scheme = HTTPBearer()

PASSWORD_HASH = PasswordHash.recommended()
settings = Settings()


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token encoding the provided data.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (Optional[timedelta]): Time until the token expires.
        Defaults to 30 minutes.

    Returns:
        str: Encoded JWT token.
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
    """Decode a JWT token into its payload.

    Args:
        token (str): JWT token string.

    Returns:
        dict: Decoded payload.
    """
    return jwt.decode(token, settings.SECRET_KEY,
                      algorithms=[settings.ALGORITHM])


def verify_password(plain: str, hashed: str) -> bool:
    """Verify that a plain password matches the hashed password.

    Args:
        plain (str): Plain-text password.
        hashed (str): Hashed password from database.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return PASSWORD_HASH.verify(plain, hashed)


def get_password_hash(plain: str) -> str:
    """Hash a plain password for storage.

    Args:
        plain (str): Plain-text password.

    Returns:
        str: Hashed password.
    """
    return PASSWORD_HASH.hash(plain)


async def authenticate_user(user: UserLogin) -> Optional[User]:
    """Authenticate a user by email and password.

    Args:
        user (UserLogin): User credentials.

    Returns:
        Optional[UserGet]: Authenticated user if credentials are correct, else
        None.
    """
    auth_user = await get_user_by_email(user.email)

    if not user:
        return None

    if not verify_password(user.password, auth_user.password):
        return None

    return auth_user

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> UserGet:
    """Retrieve the current authenticated user from a JWT token."""
    token = credentials.credentials  # <- tu bierzemy sam token z nagłówka

    if len(token) < 1:
        raise HTTPException(401, "Missing token")

    data = decode_token(token)

    if not data or data.get("type") != "access":
        raise HTTPException(401, "Invalid token")

    email = data.get("sub")

    if not email:
        raise HTTPException(401, "Invalid token")

    user = await get_user_by_email(email)

    if not user:
        raise HTTPException(401, "User not found")

    return user


async def get_current_user_ws(websocket: WebSocket) -> UserGet:
    """Retrieve the authenticated user for WebSockets using the JWT token
    passed via the WebSocket subprotocols.

    Args:
        websocket (WebSocket): Incoming WebSocket connection.

    Raises:
        HTTPException: If token is invalid or user is not found.

    Returns:
        UserGet: Authenticated user.
    """
    protocols = websocket.headers.get("sec-websocket-protocol", "")
    parts = [p.strip() for p in protocols.split(",")]

    if len(parts) < 2:
        raise HTTPException(status_code=401, detail="Missing token")

    token = parts[1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    data = decode_token(token)

    if not data or data.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token")

    email = data.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user