"""
Schemas - Index.

Theses schemas provided here are specifically designed to be used on
"SF2" infrastructure.
"""

from src.libs.schemas.base_model import BaseModel
from src.libs.schemas.messages import MessageSchema
from src.libs.schemas.utils import return_schema_example

__all__ = [
    "BaseModel",
    "MessageSchema",
    "return_schema_example",
]
