# DB接続
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# .envを読み込む
load_dotenv()


# PostgreSQLの接続URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# PostgreSQLに接続するEngine
engine = create_engine(DATABASE_URL)


# DB Sessionを作るためのsessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemyのモデルの親クラス
class Base(DeclarativeBase):
    pass


# DB Sessionを取得するDependency
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()