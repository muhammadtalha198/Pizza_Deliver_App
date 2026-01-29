from sqlite3 import IntegrityError

from fastapi import  HTTPException
from sqlmodel import Session, select
from starlette import status

from app.core.security import get_password_hash, get_user, authenticate_user, create_access_token, \
    send_verification_email
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate



class UserService:
    @staticmethod
    async def register_user(user: UserCreate, session: Session):

        existing = get_user(user.username, session)
        if existing:
            raise HTTPException(status_code=400, detail="user already registered")

        # Check if email already exists
        existing_email = session.exec(select(User).where(User.email == user.email)).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="email already registered")

        try:
            # hash the password before saving
            hashed_pwd = get_password_hash(user.password)
            new_user = User(
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                hashed_password=hashed_pwd
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # 🔥 Send email
            send_verification_email(new_user.id,new_user.email)

            return {"message": "User registered successfully", "user_id": new_user.id}

        except IntegrityError as error:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(error))
        except Exception as error:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(error))

    @staticmethod
    def login_user(form_data, session: Session):
        # Authenticate user with either username or email and password
        # The OAuth2PasswordRequestForm uses "username" field, but we accept either username or email
        user = authenticate_user(form_data.username, form_data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token and send in return
        access_token = create_access_token(data={"sub": user.username, "email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

