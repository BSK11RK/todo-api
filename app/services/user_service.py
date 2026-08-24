from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate, LoginRequest
from app.security import hash_password, verify_password, create_access_token
from app.repositories.user_repository import (
    create_user as repository_create_user,
    get_user as repository_get_user,
    get_user_by_email as repository_get_user_by_email,
    get_users as repository_get_users
)


# GET
def get_users(db: Session) -> list[User]:
    return repository_get_users(db=db)


# GET_ID
def get_user(db: Session, user_id: int) -> User:
    user = repository_get_user(db=db, user_id=user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# POST
def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = repository_get_user_by_email(db=db, email=user_data.email)
    
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )
    
    return repository_create_user(db=db, user=user)


# Login
def login_user(db: Session, login_data: LoginRequest) -> str:
    user = repository_get_user_by_email(db=db, email=login_data.email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    password_correct = verify_password(login_data.password, user.password)
    
    if not password_correct:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(user_id=user.id)
    
    return access_token