from pydantic import BaseModel, Required
from typing import Union, Optional
from fastapi import Query


class TodoBase(BaseModel):
    id: Optional[str]


class TodoCreate(BaseModel):
    title: str
    description: str
    category: str
    start_date: str
    end_date: str


class TodoUpdate(TodoBase):
    title: Optional[str]
    finish: Optional[bool]
    description: Optional[str]
    category: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]


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
