# APIの処理
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.services import todo_services
from app.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoPatch,
    TodoResponse,
    TodoQuery
)


router = APIRouter(prefix="/todos", tags=["TODOS"])


# GET
@router.get("", response_model=list[TodoResponse])
def get_todos(
    keyword: str | None = None,
    db: Session = Depends(get_db)
):
    return todo_services.get_todos(db=db, keyword=keyword)


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_services.get_todo(db=db, todo_id=todo_id)
    
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
    return todo_services.create_todo(db=db, todo_data=todo)


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, 
    todo: TodoUpdate,
    db: Session = Depends(get_db)
):
    updated_todo = todo_services.update_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo
    )
    
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return updated_todo


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int, 
    todo: TodoPatch,
    db: Session = Depends(get_db)
):
    patched_todo = todo_services.patch_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo
    )
    
    if patched_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return patched_todo


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted_todo = todo_services.delete_todo(db=db, todo_id=todo_id)
    
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return deleted_todo