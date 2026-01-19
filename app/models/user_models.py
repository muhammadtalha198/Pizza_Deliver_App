
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)

    username: str = Field(unique=True, index=True, nullable=False)
    full_name: str = Field(index=True, nullable=False)

    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)