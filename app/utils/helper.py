from fastapi import Depends, HTTPException
from sqlmodel import Session, text
from app.db.session import get_session


def check_db_ready(db: Session = Depends(get_session)):
    try:
         db.exec(text("SELECT 1"))
         db.exec(text("SELECT 1 FROM users LIMIT 1"))
    except Exception:
        raise HTTPException(status_code=500, detail="Database not ready")