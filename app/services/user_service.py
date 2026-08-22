from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate
from app.repositories.user_repository import (
    create_user as repository_create_user,
    get_user_by_email as repository_get_user_by_email
)


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = repository_get_user_by_email(db=db, email=user_data.email)
    
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        name=user_data.name,
        email=user_data.email
    )
    
    return repository_create_user(db=db, user=user)