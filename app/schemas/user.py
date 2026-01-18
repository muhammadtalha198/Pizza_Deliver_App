from pydantic import BaseModel, EmailStr

# Registration (input)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Login (input)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Response (output)
class UserToken(BaseModel):
    access_token: str
    token_type: str

