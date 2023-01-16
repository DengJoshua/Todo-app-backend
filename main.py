from sqlalchemy.orm import Session
from models import Todo, User
from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, Base, engine, get_data
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4


from jwt_handler import jwt_decode

from schemas import TodoCreate, TodoUpdate, UserBase
from routes import router, oauth2_scheme

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_data)):
    auth_token = jwt_decode(token)

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == auth_token["user_id"]).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@app.get("/")
def home():
    return {"Home Page"}


@app.get("/api/todos")
def fetch_todos(db: Session = Depends(get_data), user: UserBase = Depends(get_current_user)):
    return db.query(Todo).filter(Todo.owner_id == user.id).all()


@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: str, db: Session = Depends(get_data), user: UserBase = Depends(get_current_user)):
    return db.query(Todo).filter(Todo.id == todo_id).first()


@app.post("/api/todos")
def add_todo(todo: TodoCreate, db: Session = Depends(get_data), user: UserBase = Depends(get_current_user)):

    todo_model = Todo(id=str(uuid4()), title=todo.title,
                      description=todo.description, owner_id=user.id)
    db.add(todo_model)
    db.commit()

    return db.query(Todo).filter(Todo.owner_id == user.id).all()


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: str, todo: TodoUpdate, db: Session = Depends(get_data), user: UserBase = Depends(get_current_user)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo.finish is not None:
        todo_model.finish = todo.finish
    if todo.description is not None:
        todo_model.description = todo.description
    if todo.title is not None:
        todo_model.title = todo.title
    todo_model.owner_id = user.id

    db.commit()
    return db.query(Todo).filter(Todo.owner_id == user.id).all()


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_data), user: UserBase = Depends(get_current_user)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    db.delete(todo_model)
    db.commit()

    return db.query(Todo).filter(Todo.owner_id == user.id).all()


@app.get("/api/users")
def get_users(db: Session = Depends(get_data)):
    return db.query(User).all()


@app.get("/users/{id}")
def get_user(id: str, db: Session = Depends(get_data)):
    return db.query(User).filter(User.id == id).first()
