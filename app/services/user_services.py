from fastapi import  HTTPException
from sqlmodel import Session, select

from app.models.user_models import User
from app.schemas.user_schemas import UserCreate
from app.utils.helper import check_db_ready


class UserService:
    @staticmethod
    async def register_user(user: UserCreate, session: Session):

        #check db and table
        check_db_ready(session)

        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        # session.add(user)
        # session.commit()
        return user

        # if existing_user = session.ex


