# APIの処理
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoPatch,
    TodoResponse,
    TodoQuery
)


router = APIRouter(prefix="/todos", tags=["TODOS"])


todos = []


# Dependency
def get_todo_query(
    completed: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> TodoQuery:
    return TodoQuery(
        completed=completed,
        skip=skip,
        limit=limit
    )
    
    
# GET
@router.get("", response_model=list[TodoResponse])
def get_todos(
    params: TodoQuery = Depends(get_todo_query),
    db: Session = Depends(get_db)
):
    statement = select(Todo)
    
    if params.completed is not None:
        statement = statement.where(
            Todo.completed == params.completed
        )
        
    statement = statement.offset(params.skip).limit(params.limit)
    
    result = db.scalars(statement).all()
    
    return result


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo


# POST
@router.post(
    "", 
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(
        title=todo.title,
        completed=todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, 
    todo: TodoUpdate,
    db: Session = Depends(get_db)
):
    item = db.get(Todo, todo_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    item.title = todo.title
    item.completed = todo.completed
    
    db.commit()
    db.refresh(item)
    
    return item


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int, 
    todo: TodoPatch,
    db: Session = Depends(get_db)
):
    item = db.get(Todo, todo_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.title is not None:
        item.title = todo.title
        
    if todo.completed is not None:
        item.completed = todo.completed
        
    db.commit()
    db.refresh(item)
    
    return item


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    item = db.get(Todo, todo_id)
    
    if item is not None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(item)
    db.commit()
    
    return item