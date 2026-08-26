from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import get_current_user
from app.schemas import (
    UserCreate,
    UserPatch,
    UserResponses,
    UserUpdate
)
from app.services.user_service import (
    create_user,
    delete_user,
    patch_user,
    update_user
)


router = APIRouter(prefix="/users", tags=["Users"])


# 現在ログインしているUser
@router.get("/me", response_model=UserResponses)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# POST
@router.post(
    "",
    response_model=UserResponses,
    status_code=status.HTTP_201_CREATED
)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user_data=user)


# PUT
@router.put("/me", response_model=UserResponses)
def update_me(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_user(
        db=db,
        current_user=current_user,
        user_data=user
    )


# PATCH
@router.patch("/me", response_model=UserResponses)
def patch_me(
    user: UserPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return patch_user(
        db=db,
        current_user=current_user,
        user_data=user
    )


# DELETE
@router.delete("/me", response_model=UserResponses)
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_user(db=db, current_user=current_user)