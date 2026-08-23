from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Todo


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


# User IDからTodoを取得
def get_todos_by_user(db: Session, user_id: int) -> list[Todo]:
    statement = select(Todo).where(Todo.user_id == user_id)
    
    result = db.scalars(statement)
    
    return result.all()


# GET_ID
def get_todo(db: Session, todo_id: int) -> Todo | None:
    return db.get(Todo, todo_id)


# POST
def create_todo(db: Session, todo: Todo) -> Todo:
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return todo


# PUT & PATCH
def save_todo(db: Session, todo: Todo) -> Todo:
    db.commit()
    db.refresh(todo)
    
    return todo


# DELETE
def delete_todo(db: Session, todo: Todo) -> Todo:
    db.delete(todo)
    db.commit()
    
    return todo