from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI()


todos = []


# Pydantic
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
    

# GET
@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    return todos


# GET_ID
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
        
    raise HTTPException(status_code=404, detail="Todo not found")


# POST
@app.post(
    "/todos", 
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo:  TodoCreate):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }
    
    todos.append(new_todo)
    
    return new_todo


# PUT
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    for item in todos:
        if item["id"] == todo_id:
            item["title"] = todo.title
            item["completed"] = todo.completed
            
            return item
    
    raise HTTPException(status_code=404, detail="Todo not found")


# PATCH
@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, todo: TodoPatch):
    for item in todos:
        if item["id"] == todo_id:
            
            if todo.title is not None:
                item["title"] = todo.title
                
            if todo.completed is not None:
                item["completed"] = todo.completed
                
            return item
        
    raise HTTPException(status_code=404, detail="Todo not found")


# DELETE
@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(index)
            
            return deleted_todo
        
    raise HTTPException(status_code=404, detail="Todo not found")