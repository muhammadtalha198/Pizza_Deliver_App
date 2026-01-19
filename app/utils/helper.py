from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session
from app.db.session import get_session


def check_db_ready(db: Session = Depends(get_session)):
    try:
         db.execute(text("SELECT 1"))
         db.execute(text("SELECT 1 FROM users LIMIT 1"))
    except Exception:
        raise HTTPException(status_code=500, detail="Database not ready")