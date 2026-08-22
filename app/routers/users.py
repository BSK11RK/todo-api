from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponses
from app.services.user_service import create_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponses,
    status_code=status.HTTP_201_CREATED
)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user_data=user)