# Todoの処理
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, TodoPatch, TodoQuery


# GET
def get_todos(db: Session, params: TodoQuery) -> list[Todo]:
    statement = select(Todo)
    
    if params.completed is not None:
        statement = statement.where(
            Todo.completed == params.completed
        )
        
    statement = statement.offset(params.skip).limit(params.limit)
    
    return db.scalars(statement).all()

# GET_ID
def get_todo(db: Session, todo_id: int) -> Todo | None:
    return db.get(Todo, todo_id)


# POST
def create_todo(db: Session, todo_data: TodoCreate) -> Todo:
    todo = Todo(
        title=todo_data.title,
        completed=todo_data.completed
    )
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return todo


# PUT
def update_todo(
    db: Session,
    todo_id: int,
    todo_data: TodoUpdate
) -> Todo | None:
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        return None
    
    todo.title = todo_data.title
    todo.completed = todo_data.completed
    
    db.commit()
    db.refresh(todo)
    
    return todo


# PATCH
def patch_todo(
    db: Session,
    todo_id: int,
    todo_data: TodoPatch
) -> Todo | None:
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        return None
    
    if todo_data.title is not None:
        todo.title = todo_data.title
        
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
        
    db.commit()
    db.refresh(todo)
    
    return todo


# DELETE
def delete_todo(db: Session, todo_id: int) -> Todo | None:
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        return None
    
    db.delete(todo)
    db.commit()
    
    return todo