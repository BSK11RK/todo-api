from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LoginRequest, LoginResponse
from app.services.user_service import login_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    access_token = login_user(db=db, login_data=login_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }