from datetime import timedelta, datetime, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Session, select
from starlette import status

from app.core.config import settings
from app.models.user_models import User
from app.schemas.auth_schemas import TokenData
from app.utils.email_utils import send_email_verification


ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()

class AuthServices:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta( minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def get_user_by_username_or_email(identifier: str, session: Session) -> User | None:
        """Get user by username or email, raises error if not found"""
        user = session.exec(select(User).where(User.username == identifier)).first()

        if user is None:
            user = session.exec(select(User).where(User.email == identifier)).first()

        if user is None:
            return None

        return user


    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        verified =password_hash.verify(plain_password, hashed_password)
        return verified

    @staticmethod
    def get_password_hash(password):
        return password_hash.hash(password)

    @staticmethod
    def authenticate_user(identifier: str, password: str, session: Session):

        user = AuthServices.get_user_by_username_or_email(identifier,session)
        if user is None:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        verified = AuthServices.verify_password(password, user.hashed_password)
        if not verified:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect username or password")
        return user

    @staticmethod
    def get_current_user(token: str, session: Session) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            email = payload.get("email")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username, email=email)
        except InvalidTokenError:
            raise credentials_exception
        user = AuthServices.get_user_by_username_or_email(token_data.username,session)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    @staticmethod
    def require_admin(current_user: Annotated[User, Depends(get_current_user)])-> User:
        if not current_user.is_admin:
            raise HTTPException(status_code=400, detail="Admin required")
        return current_user

    @staticmethod
    def create_email_verification_token(user_id: str) -> str:
        """Create a JWT token for email verification."""
        expires = timedelta(hours=24)

        payload = {
            "sub": "email_verification",
            "user_id": user_id,
        }
        return AuthServices.create_access_token(payload, expires_delta=expires)

    @staticmethod
    def send_verification_email(user_id: str, user_email: str):
        """Generate email verification token and send the email."""
        token = AuthServices.create_email_verification_token(user_id)
        send_email_verification(user_email, token)