# DB接続
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# プロジェクトルート
BASE_DIR = Path(__file__).resolve().parent.parent

# dataフォルダ
DATA_DIR = BASE_DIR / "data"

# dataフォルダがなければ作成
DATA_DIR.mkdir(exist_ok=True)

# SQLiteデータベースのパス
DATABASE_URL = f"sqlite:///{DATA_DIR / 'todo.db'}"

# SQLiteに接続するEngine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


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