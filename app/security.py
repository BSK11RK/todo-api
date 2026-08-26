import os, jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.repositories.user_repository import get_user


# .envを読み込む
load_dotenv()


# パスワード
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# JWT
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# JWTをBearer Tokenとして受け取る
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# JWTを作る
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {"sub": str(user_id), "exp": expire}
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token


# JWTから現在のUserを取得する
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        user_id = int(user_id)
        
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception
    
    user = get_user(db=db, user_id=user_id)
    
    if user is None:
        raise credentials_exception
    
    return user