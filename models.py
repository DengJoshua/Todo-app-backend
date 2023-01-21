from database import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    finish = Column(Boolean, default=False)
    category = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    items = relationship("Todo", back_populates="owner")
