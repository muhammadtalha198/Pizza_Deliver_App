
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

from app.models.user_models import User
from app.services.auth_services import AuthServices


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return AuthServices.verify_password(plain_password, hashed_password)


def get_password_hash(password):
    return AuthServices.get_password_hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return AuthServices.create_access_token(data, expires_delta)
    

def decode_token(token: str) -> dict:
    return AuthServices.decode_token(token)

def get_user(username_or_email: str, session: Session) -> User | None:
    return AuthServices.get_user_by_username_or_email(username_or_email, session)

def authenticate_user(identifier: str, password: str, session: Session):
    return AuthServices.authenticate_user(identifier, password, session)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session: Session) -> User:
    return await AuthServices.get_current_user(token, session)

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return await AuthServices.get_current_active_user(current_user)

async def require_admin(current_user: Annotated[User, Depends(get_current_active_user)],) -> User:
    return await AuthServices.require_admin(current_user)




