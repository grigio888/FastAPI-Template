"""
Message Schema.
"""

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    """Generic Response Schema."""

    detail: str = Field(
        ...,
        description="A message to deliver",
        examples=["A message."],
    )
