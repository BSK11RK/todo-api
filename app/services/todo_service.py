# Todoの処理
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, TodoPatch
from app.repositories.todo_repository import (
    create_todo as repository_create_todo,
    delete_todo as repository_delete_todo,
    get_todo as repository_get_todo,
    get_todos as repository_get_todos,
    save_todo as repository_save_todo
)


# GET
def get_todos(
    db: Session,
    current_user: User,
    keyword: str | None = None,
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[Todo]:
    return repository_get_todos(
        db=db,
        user_id=current_user.id,
        keyword=keyword,
        completed=completed,
        skip=skip,
        limit=limit
    )
    

# GET_ID
def get_todo(
    db: Session, 
    todo_id: int,
    current_user: User
) -> Todo:
    todo = repository_get_todo(db=db, todo_id=todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail= "Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to access this Todo"
        )
    
    return todo


# POST
def create_todo(
    db: Session, 
    todo_data: TodoCreate,
    current_user: User
) -> Todo:
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed,
        user_id=current_user.id
    )
    
    return repository_create_todo(db=db, todo=todo)


# PUT
def update_todo(
    db: Session,
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User
) -> Todo | None:
    todo = repository_get_todo(db=db, todo_id=todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this Todo"
        )
    
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    
    return repository_save_todo(db=db, todo=todo)


# PATCH
def patch_todo(
    db: Session,
    todo_id: int,
    todo_data: TodoPatch,
    current_user: User
) -> Todo | None:
    todo = repository_get_todo(db=db, todo_id=todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this Todo"
        )
    
    if todo_data.title is not None:
        todo.title = todo_data.title
        
    if todo_data.description is not None:
        todo.description = todo_data.description
        
        todo.completed = True
        
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
        
    return repository_save_todo(db=db, todo=todo)


# DELETE
def delete_todo(
    db: Session, 
    todo_id: int,
    current_user: User
) -> Todo:
    todo = repository_get_todo(db=db, todo_id=todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this Todo"
        )
    
    return repository_delete_todo(db=db, todo=todo)