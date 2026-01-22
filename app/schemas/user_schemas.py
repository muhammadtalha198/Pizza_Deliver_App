from pydantic import BaseModel, EmailStr

# Registration (input)
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

# Login (input)
class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str

