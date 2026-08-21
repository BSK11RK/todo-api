# APIの処理
from fastapi import APIRouter, Depends, Query, status
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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_todos(
        db=db, 
        keyword=keyword, 
        completed=completed,
        skip=skip,
        limit=limit
    )


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db=db, todo_id=todo_id)
    
    return get_todo(db=db, todo_id=todo_id)


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
    return update_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo
    )


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
def patch(
    todo_id: int, 
    todo: TodoPatch,
    db: Session = Depends(get_db)
):
    return patch_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo
    )


# DELETE
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete(todo_id: int, db: Session = Depends(get_db)):
    return delete_todo(db=db, todo_id=todo_id)