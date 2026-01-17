from fastapi import APIRouter, Depends
from sqlmodel import Session, text

from app.db.session import get_session

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/health/db")
def health_db(session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return {"db": "ok"}
