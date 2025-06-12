from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)     
    hashed_password: str
    role: str = Field(default="cliente")
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    email: EmailStr        
    password: str


class UserRead(SQLModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
