# APIのデータの形
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool = False
    
    
class TodoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool
    
    
class TodoPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None
    
    
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    

# Query Parameter用
class TodoQuery(BaseModel):
    completed: bool | None = None
    skip: int = 0
    limit: int = 10