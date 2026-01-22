from pydantic import BaseModel, EmailStr


# Token Response (output)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
