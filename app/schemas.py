# APIのデータの形
from datetime import datetime
from pydantic import BaseModel, Field


# User
class UserCreate(BaseModel):
    name: str
    email: str
    
    
class UserResponses(BaseModel):
    id: int
    name: str
    email: str


# Todo
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool = False
    
    
class TodoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool
    
    
class TodoPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None
    
    
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    

# Query Parameter用
class TodoQuery(BaseModel):
    completed: bool | None = None
    skip: int = 0
    limit: int = 10