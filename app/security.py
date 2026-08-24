from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


# パスワード
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# JWT
SECRET_KEY = "change-this-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {"sub": str(user_id), "exp": expire}
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token