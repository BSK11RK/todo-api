# APIの処理
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    TodoCreate,
    TodoPatch,
    TodoResponse,
    TodoUpdate
)
from app.services.todo_service import (
    create_todo,
    delete_todo,
    get_todo,
    get_todos,
    patch_todo,
    update_todo
)


router = APIRouter(prefix="/todos", tags=["TODOS"])


# GET
@router.get("", response_model=list[TodoResponse])
def read_todos(
    keyword: str | None = None,
    completed: bool | None = None,
    db: Session = Depends(get_db)
):
    return get_todos(db=db, keyword=keyword, completed=completed)


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db=db, todo_id=todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo


# POST
@router.post(
    "", 
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, todo_data=todo)


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update(
    todo_id: int, 
    todo: TodoUpdate,
    db: Session = Depends(get_db)
):
    updated_todo = update_todo(db=db, todo_id=todo_id, todo_data=todo)
    
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return updated_todo


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch(
    todo_id: int, 
    todo: TodoPatch,
    db: Session = Depends(get_db)
):
    patched_todo = patch_todo(db=db, todo_id=todo_id, todo_data=todo)
    
    if patched_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return patched_todo


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete(todo_id: int, db: Session = Depends(get_db)):
    deleted_todo = delete_todo(db=db, todo_id=todo_id)
    
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return deleted_todo