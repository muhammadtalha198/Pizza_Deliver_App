
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
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: Session = Depends(get_session)):
    return UserService.login_user(form_data, session)


