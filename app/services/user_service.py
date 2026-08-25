from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate, UserUpdate, UserPatch
from app.security import hash_password, verify_password, create_access_token
from app.repositories.user_repository import (
    create_user as repository_create_user,
    delete_user as repository_delete_user,
    get_user as repository_get_user,
    get_user_by_email as repository_get_user_by_email,
    get_users as repository_get_users,
    save_user as repository_save_user
)


# GET
def get_users(db: Session) -> list[User]:
    return repository_get_users(db=db)


# GET_ID
def get_user(db: Session, user_id: int) -> User:
    user = repository_get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# POST
def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = repository_get_user_by_email(
        db=db,
        email=user_data.email
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    return repository_create_user(db=db, user=user)


# Login
def login_user(
    db: Session,
    email: str,
    password: str
) -> str:
    user = repository_get_user_by_email(db=db, email=email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = verify_password(password, user.password)

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user_id=user.id)

    return access_token


# PUT
def update_user(
    db: Session,
    current_user: User,
    user_data: UserUpdate
) -> User:
    # メールアドレスが変更される場合
    if user_data.email != current_user.email:

        existing_user = repository_get_user_by_email(
            db=db,
            email=user_data.email
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    current_user.name = user_data.name
    current_user.email = user_data.email

    return repository_save_user(db=db, user=current_user)


# PATCH
def patch_user(
    db: Session,
    current_user: User,
    user_data: UserPatch
) -> User:
    # 名前が指定されていたら更新
    if user_data.name is not None:
        current_user.name = user_data.name

    # メールアドレスが指定されていたら更新
    if user_data.email is not None:

        if user_data.email != current_user.email:

            existing_user = repository_get_user_by_email(
                db=db,
                email=user_data.email
            )

            if existing_user is not None:
                raise HTTPException(
                    status_code=400, 
                    detail="Email already registered"
            )
            
        current_user.email = user_data.email

    return repository_save_user(db=db, user=current_user)


# DELETE
def delete_user(db: Session, current_user: User) -> User:
    return repository_delete_user(db=db, user=current_user)