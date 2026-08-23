from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponses
from app.services.user_service import create_user, get_user, get_users


router = APIRouter(prefix="/users", tags=["Users"])


# GET
@router.get("", response_model=list[UserResponses])
def read_users(db: Session = Depends(get_db)):
    return get_users(db=db)


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