import jwt
from jwt import InvalidTokenError
from sqlmodel import Session, select
from starlette import status
from typing import Annotated
from fastapi import HTTPException, Depends

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

from app.models.user_models import User
from app.schemas.auth_schemas import TokenData
from app.services.auth_services import AuthServices


ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return AuthServices.verify_password(plain_password, hashed_password)


def get_password_hash(password):
    return AuthServices.get_password_hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return AuthServices.create_access_token(data, expires_delta)
    

def decode_token(token: str) -> dict:
    # raises InvalidTokenError if invalid
    return AuthServices.decode_token(token)



def get_user(username_or_email: str, session: Session) -> User | None:
    """Get user by either username or email"""
    return AuthServices.get_user_by_username_or_email(username_or_email, session)

def authenticate_user(identifier: str, password: str, session: Session):
    """Authenticate user with either username or email"""
    return AuthServices.authenticate_user(identifier, password, session)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
    session: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_admin(current_user: Annotated[User, Depends(get_current_active_user)],) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user




