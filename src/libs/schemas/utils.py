"""
Schemas - Utilities.
"""

from pydantic import BaseModel


def return_schema_example(schema: type[BaseModel]) -> dict:
    """
    Return the schema example.

    This function will return the schema example, meant to be used on route
    responses example.

    Example:
    ```
    @router.post(
        path="/todo",
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {
                "model": ToDoSchema,
                "description": "ToDo created successfully.",
                "content": {
                    "application/json": {
                        "example": return_schema_example(ToDoSchema),
                    },
                },
            },
            ...
        },
    )
    async def create_todo(
        todo_data: ToDoSchema,
    ) -> ToDoSchema:

    return await services.create_new_todo(todo_data)
    ```

    """

    return {
        field: desc.examples[0] if desc.examples else desc.default
        for field, desc in schema.model_fields.items()
    }
