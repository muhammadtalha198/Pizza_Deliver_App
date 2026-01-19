from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session

from app.schemas.user_schemas import UserCreate
from app.services.user_services import UserService

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    return await UserService.register_user(user, session)


# @router.post("/login", response_model=UserToken)
# def login_user(user: UserLogin, session: Session = Depends(get_session)):
#     db_user = session.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#
#     # Generate JWT token for the user
#     access_token = create_access_token(data={"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}
