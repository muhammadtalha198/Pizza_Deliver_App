from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.user import User
from app.core.auth import verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/me")
def get_user_info(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = session.query(User).filter(User.email == payload["sub"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": db_user.email, "is_admin": db_user.is_admin}
