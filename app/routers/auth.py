from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LoginResponse
from app.services.user_service import login_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    access_token = login_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }