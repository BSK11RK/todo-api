from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponses, TodoResponse, TodoCreate
from app.services.user_service import create_user, get_user, get_users
from app.services.todo_service import get_todos_by_user, create_todo_for_user


router = APIRouter(prefix="/users", tags=["Users"])


# GET
@router.get("", response_model=list[UserResponses])
def read_users(db: Session = Depends(get_db)):
    return get_users(db=db)


# UserのTodoを取得
@router.get("/{user_id}/todos", response_model=list[TodoResponse])
def read_user_todos(user_id: int, db: Session = Depends(get_db)):
    # Userが存在するか確認
    get_user(db=db, user_id=user_id)
    
    return get_todos_by_user(db=db, user_id=user_id)


# UserにTodoを作成
@router.post(
    "/{user_id}/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user_todo(
    user_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    # Userが存在するか確認
    get_user(db=db, user_id=user_id)
    
    return create_todo_for_user(
        db=db,
        user_id=user_id,
        todo_data=todo
    )


# GET_ID
@router.get("/{user_id}", response_model=UserResponses)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)


# POST
@router.post(
    "",
    response_model=UserResponses,
    status_code=status.HTTP_201_CREATED
)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user_data=user)