
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from starlette import status

from app.core.security import authenticate_user, create_access_token
from app.db.session import get_session
from app.schemas.auth_schemas import Token

from app.schemas.user_schemas import UserCreate
from app.services.user_services import UserService

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    return await UserService.register_user(user, session)



@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    # Authenticate user with either username or email and password
    # The OAuth2PasswordRequestForm uses "username" field, but we accept either username or email
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}