from pydantic import BaseModel, EmailStr

# Registration (input)
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    hashed_password: str

# Login (input)
class UserLogin(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

# Token Response (output)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
