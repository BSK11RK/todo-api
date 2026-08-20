from fastapi import FastAPI

import app.models
from app.database import Base, engine
from app.routers.todos import router as todo_router


app = FastAPI()


# テーブル作成
Base.metadata.create_all(bind=engine)


app.include_router(todo_router)