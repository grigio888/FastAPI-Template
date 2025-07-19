"""
ToDo - Service.

This module contains the business logic for the todo service.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

if TYPE_CHECKING:
    from src.libs.pagination.schema import PaginatedSchema

from src.apps.todos.models import TodoModel
from src.apps.todos.schemas import (
    TodoDataSchema,
    TodoSchema,
)
from src.libs.database.pagination import paginate
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.messages import Messages

log = get_logger()


async def list_todos(page: int, limit: int) -> PaginatedSchema:
    """
    Paginate todos.

    Note: This method uses a simple pagination, but when dealing with salesforce
    models, we need to use the pagination provided in the ORM.
    """

    log.debug(f"{_()}: Listing todos with page {page} and limit {limit}")

    return paginate(
        model=TodoModel,
        page=page,
        page_size=limit,
        schema=TodoSchema,
    )


def get_todo(todo_id: int) -> TodoSchema:
    """
    Get todo by ID.
    """

    log.debug(f"{_()}: Getting todo with ID {todo_id}")

    todo = TodoModel.query().filter(TodoModel.id == todo_id).first()

    if not todo:
        message = Messages.TODO_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: Todo found: {todo}")

    return TodoSchema.from_model(todo)


def create_todo(data: TodoDataSchema) -> TodoSchema:
    """
    Create a new todo.

    This function will create a new todo with the provided data.
    """

    log.debug(f"{_()}: Creating todo with data: {data}")
    log.debug(f"{_()}: Fetching last todo id")

    todo_model = TodoModel(
        **data.model_dump(exclude_unset=True),
    )

    todo_model.save()

    return TodoSchema.from_model(todo_model)


def update_todo(todo_id: int, data: TodoDataSchema) -> TodoSchema:
    """
    Update a todo.

    This function will update a todo with the provided data.
    """

    log.debug(f"{_()}: Updating todo with ID {todo_id} and data: {data}")

    todo_model = TodoModel.query().filter(TodoModel.id == todo_id).first()

    if not todo_model:
        message = Messages.TODO_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: Todo found: {todo_model}")
    log.debug(f"{_()}: Updating todo with data: {data}")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(todo_model, key, value)

    return TodoSchema.from_model(todo_model)


def delete_todo(todo_id: int) -> None:
    """
    Delete a todo.

    This function will delete a todo by its ID.
    """

    log.debug(f"{_()}: Deleting todo with ID {todo_id}")

    todo_model = TodoModel.query().filter(TodoModel.id == todo_id).first()

    if not todo_model:
        message = Messages.TODO_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: Todo found: {todo_model}")
    log.debug(f"{_()}: Deleting todo from list.")

    todo_model.delete()

    log.debug(f"{_()}: Todo deleted from list: {todo_model}")
