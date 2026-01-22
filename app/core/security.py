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
from app.db.session import get_session
from app.models.user_models import User
from app.schemas.auth_schemas import TokenData


ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    # raises InvalidTokenError if invalid
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

def get_user(username: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()

def get_user_by_email(email: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_username_or_email(identifier: str, session: Session) -> User | None:
    """Get user by either username or email"""
    # Try username first
    user = get_user(identifier, session)
    if user:
        return user
    # Try email if username not found
    return get_user_by_email(identifier, session)

def authenticate_user(identifier: str, password: str, session: Session):
    """Authenticate user with either username or email"""
    user = get_user_by_username_or_email(identifier, session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session)
):
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




