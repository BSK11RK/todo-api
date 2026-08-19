from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoPatch,
    TodoResponse,
    TodoQuery
)


router = APIRouter(prefix="/todos", tags=["TODOS"])


todos = []


# Dependency
def get_todo_query(
    completed: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> TodoQuery:
    return TodoQuery(
        completed=completed,
        skip=skip,
        limit=limit
    )
    
    
# GET
@router.get("", response_model=list[TodoResponse])
def get_todos(params: TodoQuery = Depends(get_todo_query)):
    filtered_todos = todos
    
    if params.completed is not None:
        filtered_todos = [
            todos
            for todo in filtered_todos
            if todo["completed"] == params.completed
        ]
        
    filtered_todos = filtered_todos[params.skip:params.skip + params.limit]
    
    return filtered_todos


# GET_ID
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
        
    raise HTTPException(status_code=404, detail="Todo not found")


# POST
@router.post(
    "", 
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: TodoCreate):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }

    todos.append(new_todo)
    
    return new_todo


# PUT
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    for item in todos:
        if item["id"] == todo_id:
            item["title"] = todo.title
            item["completed"] = todo.completed

            return item
        
    raise HTTPException(status_code=404, detail="Todo not found")


# PATCH
@router.patch("/{todo_id}", response_model=TodoResponse)
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
@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(index)
            
            return deleted_todo
        
    raise HTTPException(status_code=404, detail="Todo not found")