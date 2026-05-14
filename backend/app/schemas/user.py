from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=6
    )


class UserRead(BaseModel):

    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):

    email: EmailStr
    password: str