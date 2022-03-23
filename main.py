"""
todo app
"""
from uuid import UUID, uuid4
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Todo(BaseModel):
    id: Optional[UUID] = uuid4()
    description: str
    done: bool = False

app = FastAPI()

todo_list = [{"id": uuid4(), "done": False,
              "description": "writeme"}]


@app.get("/")
def root():
    """
    return something from root
    """
    return {'msg': 'Hello World'}


@app.get("/todo")
def get_all_todos():
    """
    return all todos
    """
    return todo_list


@app.get("/todo/completed")
def get_done():
    """
    get completed todos
    """
    return [todo for todo in todo_list if todo["done"] is True]


@app.get("/todo/pending")
def get_pending():
    """
    get pending todos
    """
    return [todo for todo in todo_list if todo["done"] is False]


@app.post("/todo")
def create_todo(todo: Todo):
    """
    create todo
    """
    todo.id = uuid4()
    todo_list.append(todo)
    return todo


@app.put("/todo/{todo_id}")
def update_todo(todo_id: UUID, todo: Todo):
    """
    update todo
    """
    for item in todo_list:
        if item["id"] == todo_id:
            if todo.done is not None:
                item["done"] = todo.done
            if todo.description is not None:
                item["description"] = todo.description
            return
    raise HTTPException(
        status_code=404, detail=f"todo id: {todo_id} not found")


@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: UUID):
    """
    delete todo
    """
    result = next((i for i, item in enumerate(
        todo_list) if item["id"] == todo_id), None)
    if result is not None:
        del todo_list[result]
    else:
        raise HTTPException(
            status_code=404, detail=f"todo id: {todo_id} not found")
