"""
Test Schemas Module.

This module tests the schema utilities and base model in src/libs/schemas/.
"""

import unittest
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, Field

from src.libs.schemas.base_model import BaseModel as LibsBaseModel
from src.libs.schemas.messages import MessageSchema
from src.libs.schemas.utils import return_schema_example


class TestSchema(LibsBaseModel):
    """Test schema for testing purposes."""

    name: str = Field(..., description="Name field", examples=["John Doe"])
    age: int = Field(default=25, description="Age field", examples=[25])
    email: str = Field(..., description="Email field", examples=["john@example.com"])
    is_active: bool = Field(default=True, description="Active status", examples=[True])


class TestSchemaWithDefaults(BaseModel):
    """Test schema with default values."""

    title: str = Field(default="Default Title", description="Title field")
    count: int = Field(default=0, description="Count field")
    enabled: bool = Field(default=False, description="Enabled field")


class TestSchemasModule(unittest.TestCase):
    """Test schemas module functionality."""

    def test_message_schema_creation(self) -> None:
        """Test MessageSchema can be created."""
        message = MessageSchema(detail="Test message")

        assert message.detail == "Test message"

    def test_message_schema_validation(self) -> None:
        """Test MessageSchema validation."""
        # Valid message
        message = MessageSchema(detail="Valid message")
        assert isinstance(message, MessageSchema)

        # Invalid message (missing detail)
        with pytest.raises(ValueError):  # noqa: PT011
            MessageSchema()  # type: ignore  # noqa: PGH003

    def test_base_model_from_model(self) -> None:
        """Test BaseModel.from_model method."""
        # Mock a database model
        mock_db_model = MagicMock()
        mock_db_model.to_dict.return_value = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com",
            "is_active": True,
        }

        # Convert to Pydantic model
        schema_instance = TestSchema.from_model(mock_db_model)

        assert isinstance(schema_instance, TestSchema)
        assert schema_instance.name == "John Doe"
        assert schema_instance.age == 30
        assert schema_instance.email == "john@example.com"
        assert schema_instance.is_active is True

        # Verify to_dict was called
        mock_db_model.to_dict.assert_called_once()

    def test_return_schema_example_with_examples(self) -> None:
        """Test return_schema_example with schema that has examples."""
        result = return_schema_example(TestSchema)

        expected = {
            "name": "John Doe",
            "age": 25,
            "email": "john@example.com",
            "is_active": True,
        }

        assert result == expected

    def test_return_schema_example_with_defaults(self) -> None:
        """Test return_schema_example with schema that has default values."""
        result = return_schema_example(TestSchemaWithDefaults)

        expected = {
            "title": "Default Title",
            "count": 0,
            "enabled": False,
        }

        assert result == expected

    def test_return_schema_example_mixed_fields(self) -> None:
        """Test return_schema_example with mixed fields (examples and defaults)."""

        class MixedSchema(BaseModel):
            with_example: str = Field(..., examples=["Example Value"])
            with_default: int = Field(42)
            with_both: str = Field("Default", examples=["Example"])

        result = return_schema_example(MixedSchema)

        expected = {
            "with_example": "Example Value",
            "with_default": 42,
            "with_both": "Example",  # Should prefer example over default
        }

        assert result == expected

    def test_return_schema_example_multiple_examples(self) -> None:
        """Test return_schema_example when field has multiple examples."""

        class MultiExampleSchema(BaseModel):
            field: str = Field(..., examples=["First", "Second", "Third"])

        result = return_schema_example(MultiExampleSchema)

        # Should use first example
        expected = {"field": "First"}
        assert result == expected

    def test_return_schema_example_empty_schema(self) -> None:
        """Test return_schema_example with empty schema."""

        class EmptySchema(BaseModel):
            pass

        result = return_schema_example(EmptySchema)

        assert result == {}

    def test_base_model_inheritance(self) -> None:
        """Test that LibsBaseModel inherits from PydanticBaseModel."""
        assert issubclass(LibsBaseModel, BaseModel)

    def test_base_model_instantiation(self) -> None:
        """Test that LibsBaseModel can be instantiated."""

        class ConcreteModel(LibsBaseModel):
            name: str
            value: int

        instance = ConcreteModel(name="test", value=123)

        assert instance.name == "test"
        assert instance.value == 123

    def test_message_schema_field_properties(self) -> None:
        """Test MessageSchema field properties."""
        schema_fields = MessageSchema.model_fields

        assert "detail" in schema_fields

        detail_field = schema_fields["detail"]
        assert detail_field.description == "A message to deliver"
        assert detail_field.examples == ["A message."]


if __name__ == "__main__":
    unittest.main()
