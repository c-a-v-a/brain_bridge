"""
"""

from fastapi import APIRouter, Depends, HTTPException, status

from crud.user import create_user, get_user_by_email, get_user_by_username
from internals.auth import authenticate_user, create_token, get_current_user
from models.user import User, UserGet, UserLogin, UserUpdate
from models.token import TokenPair
from settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])
setting = Settings()


@router.post(
    "/register",
    response_description="Get infromation about newly created user account",
    response_model=UserGet,
    status_code=201
)
def register(user: User):
    """Create new user."""
    if get_user_by_email(user.email):
        raise HTTPException(409, "Email already taken")
    if get_user_by_username(user.username):
        raise HTTPException(409, "Username already taken")

    new_user = create_user(user)

    return new_user


@router.post(
    "/login",
    response_description="Retrieves a token pair for user",
    response_model=TokenPair
)
def login(user: UserLogin):
    """Create a pair of acess and refresh tokens for user to obtain."""
    auth_user = authenticate_user(user)

    if not user:
        raise HTTPException(401, "Incorrect email or password")

    return TokenPair(
        access_token = create_token(auth_user.email, Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token = create_token(auth_user.email, Settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


@router.post(
    "/refresh",
    response_description="Refreshes a user token pair if the refresh token is valid",
    response_model=TokenPair
)
def refresh(refresh_token: str):
    """Create new token pair if refresh token is valid."""
    data = decode_token(refresh_token)

    if not data or data.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    email = data.get("sub")
    user = get_user_by_email(email)

    if not user:
        raise HTTPException(401, "User does not exist")

    return TokenPair(
        access_token = create_token(auth_user.email, Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token = create_token(auth_user.email, Settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


@router.get(
    "/me",
    response_description="Get current user",
    response_model=UserGet
)
def me(user: UserGet = Depends(get_current_user)):
    """Return current active user."""
    return user


@router.get("/admin", response_description="Ok if the user has admin capabilities")
def admin(user: UserGet = Depends(get_current_user)):
    """Check if the user is an admin and send a response."""
    if user.isAdmin:
        return {"ok": True}
    else:
        return {"ok": False}
