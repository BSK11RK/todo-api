# Todoの処理
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, TodoPatch


# GET
def get_todos(
    db: Session, 
    keyword: str | None = None,
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[Todo]:
    statement = select(Todo)
    
    if keyword:
        statement = statement.where(Todo.title.contains(keyword))
    
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
        
    statement = statement.offset(skip).limit(limit)
        
    result = db.scalars(statement)
    
    return result.all()


# GET_ID
def get_todo(db: Session, todo_id: int) -> Todo | None:
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail= "Todo not found")
    
    return todo


# POST
def create_todo(db: Session, todo_data: TodoCreate) -> Todo:
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
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
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = todo_data.title
    todo.description = todo_data.description
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
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_data.title is not None:
        todo.title = todo_data.title
        
    if todo_data.description is not None:
        todo.description = todo_data.description
        
        todo.completed = True
        
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
        
    db.commit()
    db.refresh(todo)
    
    return todo


# DELETE
def delete_todo(db: Session, todo_id: int) -> Todo | None:
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return todo