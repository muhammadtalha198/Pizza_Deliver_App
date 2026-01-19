from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.user_models import User

router = APIRouter()



@router.get("/me")
def read_user_me(current_user: Annotated[User,Depends(get_current_user)]):
    return current_user




