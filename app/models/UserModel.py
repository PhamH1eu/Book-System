from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: str | None = None
    full_name: str | None = None


class UserCreate(User):
    password: str


class UserInDB(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
