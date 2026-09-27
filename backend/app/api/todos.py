from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.core.db import SessionDep
from app.models.todo import Todo, TodoCreate, TodoPublic, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, session: SessionDep):
    todo = Todo.model_validate(todo_in)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("", response_model=list[TodoPublic])
def read_todos(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return session.exec(select(Todo).offset(offset).limit(limit)).all()


@router.get("/{todo_id}", response_model=TodoPublic)
def read_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(todo_id: int, todo_in: TodoUpdate, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.sqlmodel_update(todo_in.model_dump(exclude_none=True))
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
