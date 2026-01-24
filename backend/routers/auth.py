"""FastAPI router for user authentication: registration, login, token refresh,
and current user info.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException

from crud.user import create_user, get_users, get_user
from internals.auth import authenticate_user, create_token, decode_token, get_current_user
from models.user import User, UserGet, UserLogin, UserFilter
from models.token import TokenPair
from settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = Settings()


@router.post(
    "/register",
    response_description="Information about newly created user account",
    response_model=UserGet,
    status_code=201
)
async def register(user: User) -> UserGet:
    """Register a new user.

    Raises:
        HTTPException: If the email or username is already taken.

    Returns:
        UserGet: Newly created user (without password).
    """
    if await len(get_users(UserFilter(email=user.email))) > 0:
        raise HTTPException(409, "Email already taken")
    if await len(get_users(UserFilter(username=user.username))) > 0:
        raise HTTPException(409, "Username already taken")

    new_user = await create_user(user)

    return new_user


@router.post(
    "/login",
    response_description="A access and refresh token pair for user",
    response_model=TokenPair
)
async def login(user: UserLogin) -> TokenPair:
    """Authenticate user and return access and refresh tokens.

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        TokenPair: Access and refresh JWT tokens.
    """
    auth_user = await authenticate_user(user)

    if auth_user is None:
        raise HTTPException(401, "Incorrect email or password")

    return TokenPair(
        access_token = create_token(
            {"sub": auth_user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        refresh_token = create_token(
            {"sub": auth_user.email, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )


@router.post(
    "/refresh",
    response_description="User's new token pair",
    response_model=TokenPair
)
async def refresh(tokens: TokenPair) -> TokenPair:
    """Refresh access and refresh tokens using a valid refresh token.

    Raises:
        HTTPException: If the refresh token is invalid or the user does not
        exist.

    Returns:
        TokenPair: New access and refresh JWT tokens.
    """
    data = decode_token(tokens.refresh_token)

    if not data or data.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    email = data.get("sub")
    users = await get_users(UserFilter(email=email))

    if not users or len(users) == 0:
        raise HTTPException(401, "User does not exist")

    user = users[0]

    return TokenPair(
        access_token = create_token(
            {"sub": user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        refresh_token = create_token(
            {"sub": user.email, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )


@router.get(
    "/validate",
    response_description="Currently authenticated user",
    response_model=UserGet
)
async def validate(user: UserGet = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return user


@router.get(
    "/admin",
    response_description="Information about user's privileges"
)
def admin(user: UserGet = Depends(get_current_user)):
    """
    Check if the current user is an admin.

    Returns:
        dict: {"admin": True} if admin, else {"admin": False}.
    """
    if user.isAdmin:
        return {"admin": True}
    else:
        return {"admin": False}
