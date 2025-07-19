"""
ToDo - Endpoints.

This module contains the endpoints for the ToDo.
"""

from fastapi import APIRouter, Query, status

from src.apps.todos import services as todos
from src.apps.todos.schemas import TodoDataSchema, TodoSchema
from src.libs.pagination.schema import PaginatedSchema
from src.libs.schemas import MessageSchema
from src.messages import Messages

router = APIRouter(prefix="/todos", tags=["To-Do"])


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": PaginatedSchema[TodoSchema],
            "description": "List of todos",
        },
    },
)
async def list_todos(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedSchema[TodoSchema]:
    """
    List a page with todos.

    This endpoint will return a object of a page the todos in it.
    """

    return await todos.list_todos(page, limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": TodoSchema,
            "description": "Todo created successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.TODO_POST_ERROR,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.TODO_POST_ERROR,
                    },
                },
            },
        },
    },
)
def create_todo(data: TodoDataSchema) -> TodoSchema:
    """
    Create a new todo.

    This endpoint will create a new todo with the provided data.
    """

    return todos.create_todo(data)


@router.get(
    "/{todo_id}",
    responses={
        status.HTTP_200_OK: {
            "model": TodoSchema,
            "description": "Todo found",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.TODO_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.TODO_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_todo(todo_id: int) -> TodoSchema:
    """
    Get a todo.

    This endpoint will return a todo by its ID.
    """

    return todos.get_todo(todo_id)


@router.put(
    "/{todo_id}",
    responses={
        status.HTTP_200_OK: {
            "model": TodoSchema,
            "description": "Todo updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.TODO_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.TODO_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def update_todo(todo_id: int, data: TodoDataSchema) -> TodoSchema:
    """
    Update a todo.

    This endpoint will update a todo by its ID.
    """

    return todos.update_todo(todo_id, data)


@router.delete(
    "/{todo_id}",
    status_code=204,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Todo deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.TODO_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.TODO_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def delete_todo(todo_id: int) -> None:
    """
    Delete a todo.

    This endpoint will delete a todo by its ID.
    """

    todos.delete_todo(todo_id)
