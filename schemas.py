from pydantic import BaseModel
from typing import Union, Optional


class TodoBase(BaseModel):
    id: Optional[str]


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(TodoBase):
    title: Optional[str]
    finish: Optional[bool]
    description: Optional[str]


class TodoDelete(TodoBase):
    pass


class UserBase(BaseModel):
    id: str
    email: str
    username: str
    hashed_password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
