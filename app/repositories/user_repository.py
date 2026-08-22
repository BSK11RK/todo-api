from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


# GET
def get_users(db: Session) -> list[User]:
    statement = select(User)
    
    result = db.scalars(statement)
    
    return result.all()


# GET_ID
def get_user(db:Session, user_id: int) -> User | None:
    return db.get(User, user_id)


# メールアドレスからUserを探す
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(
        User.email == email
    ).first()
    

# POST
def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user