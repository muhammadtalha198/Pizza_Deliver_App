from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.user import User
from app.core.auth import hash_password, create_access_token
from app.schemas.user import UserCreate, UserToken,UserLogin


router = APIRouter()


@router.post("/register", response_model=UserToken)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists using select query
    stmt = select(User).filter(User.email == user.email)
    db_user = session.execute(stmt).scalar_one_or_none()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create new user and save to DB
    new_user = User(email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token for the user
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=UserToken)
def login_user(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token for the user
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
