"""
Test Pagination Schema.

This module tests the pagination schema in src/libs/pagination/schema.py.
"""

import unittest
from typing import Any

from pydantic import BaseModel, ValidationError

from src.libs.pagination.schema import PaginatedSchema


class TestItem(BaseModel):
    """Test item for pagination testing."""

    id: int
    name: str


class TestPaginationSchema(unittest.TestCase):
    """Test pagination schema functionality."""

    def test_paginated_schema_creation(self):
        """Test creating a PaginatedSchema instance."""
        items = [
            TestItem(id=1, name="Item 1"),
            TestItem(id=2, name="Item 2"),
        ]

        paginated = PaginatedSchema[TestItem](
            count=2,
            items=items,
            next_page=2,
            previous_page=None,
            total_pages=5,
            per_page=10,
            current_page=1,
        )

        self.assertEqual(paginated.count, 2)
        self.assertEqual(len(paginated.items), 2)
        self.assertEqual(paginated.items[0].id, 1)
        self.assertEqual(paginated.items[0].name, "Item 1")
        self.assertEqual(paginated.next_page, 2)
        self.assertIsNone(paginated.previous_page)
        self.assertEqual(paginated.total_pages, 5)
        self.assertEqual(paginated.per_page, 10)
        self.assertEqual(paginated.current_page, 1)

    def test_paginated_schema_empty_items(self):
        """Test PaginatedSchema with empty items list."""
        paginated = PaginatedSchema[TestItem](
            count=0,
            items=[],
            next_page=None,
            previous_page=None,
            total_pages=0,
            per_page=10,
            current_page=1,
        )

        self.assertEqual(paginated.count, 0)
        self.assertEqual(len(paginated.items), 0)
        self.assertIsNone(paginated.next_page)
        self.assertIsNone(paginated.previous_page)
        self.assertEqual(paginated.total_pages, 0)

    def test_paginated_schema_with_dict_items(self):
        """Test PaginatedSchema with dictionary items."""
        items = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]

        paginated = PaginatedSchema[dict[str, Any]](
            count=2,
            items=items,
            next_page=None,
            previous_page=1,
            total_pages=2,
            per_page=5,
            current_page=2,
        )

        self.assertEqual(paginated.count, 2)
        self.assertEqual(len(paginated.items), 2)
        self.assertEqual(paginated.items[0]["id"], 1)
        self.assertEqual(paginated.items[1]["name"], "Item 2")
        self.assertIsNone(paginated.next_page)
        self.assertEqual(paginated.previous_page, 1)

    def test_paginated_schema_first_page(self):
        """Test PaginatedSchema for first page scenario."""
        items = [TestItem(id=i, name=f"Item {i}") for i in range(1, 11)]

        paginated = PaginatedSchema[TestItem](
            count=10,
            items=items,
            next_page=2,
            previous_page=None,
            total_pages=3,
            per_page=10,
            current_page=1,
        )

        self.assertIsNone(paginated.previous_page)
        self.assertEqual(paginated.next_page, 2)
        self.assertEqual(paginated.current_page, 1)

    def test_paginated_schema_middle_page(self):
        """Test PaginatedSchema for middle page scenario."""
        items = [TestItem(id=i, name=f"Item {i}") for i in range(11, 21)]

        paginated = PaginatedSchema[TestItem](
            count=10,
            items=items,
            next_page=3,
            previous_page=1,
            total_pages=3,
            per_page=10,
            current_page=2,
        )

        self.assertEqual(paginated.previous_page, 1)
        self.assertEqual(paginated.next_page, 3)
        self.assertEqual(paginated.current_page, 2)

    def test_paginated_schema_last_page(self):
        """Test PaginatedSchema for last page scenario."""
        items = [TestItem(id=i, name=f"Item {i}") for i in range(21, 25)]

        paginated = PaginatedSchema[TestItem](
            count=4,
            items=items,
            next_page=None,
            previous_page=2,
            total_pages=3,
            per_page=10,
            current_page=3,
        )

        self.assertEqual(paginated.previous_page, 2)
        self.assertIsNone(paginated.next_page)
        self.assertEqual(paginated.current_page, 3)

    def test_paginated_schema_single_page(self):
        """Test PaginatedSchema for single page scenario."""
        items = [TestItem(id=1, name="Only Item")]

        paginated = PaginatedSchema[TestItem](
            count=1,
            items=items,
            next_page=None,
            previous_page=None,
            total_pages=1,
            per_page=10,
            current_page=1,
        )

        self.assertIsNone(paginated.previous_page)
        self.assertIsNone(paginated.next_page)
        self.assertEqual(paginated.total_pages, 1)
        self.assertEqual(paginated.current_page, 1)

    def test_paginated_schema_required_fields(self):
        """Test that required fields are enforced."""
        with self.assertRaises(ValidationError):
            PaginatedSchema[TestItem]()

        with self.assertRaises(ValidationError):
            PaginatedSchema[TestItem](count=10)

        with self.assertRaises(ValidationError):
            PaginatedSchema[TestItem](
                count=10,
                items=[TestItem(id=1, name="Item 1")],
                # Missing required fields
            )

    def test_paginated_schema_field_types(self):
        """Test field type validation."""
        items = [TestItem(id=1, name="Item 1")]

        # Valid instance
        paginated = PaginatedSchema[TestItem](
            count=1,
            items=items,
            next_page=None,
            previous_page=None,
            total_pages=1,
            per_page=10,
            current_page=1,
        )

        self.assertIsInstance(paginated.count, int)
        self.assertIsInstance(paginated.items, list)
        self.assertIsInstance(paginated.total_pages, int)
        self.assertIsInstance(paginated.per_page, int)
        self.assertIsInstance(paginated.current_page, int)

    def test_paginated_schema_optional_fields(self):
        """Test that next_page and previous_page are optional."""
        items = [TestItem(id=1, name="Item 1")]

        # Should work without next_page and previous_page
        paginated = PaginatedSchema[TestItem](
            count=1,
            items=items,
            total_pages=1,
            per_page=10,
            current_page=1,
        )

        self.assertIsNone(paginated.next_page)
        self.assertIsNone(paginated.previous_page)

    def test_paginated_schema_serialization(self):
        """Test PaginatedSchema serialization."""
        items = [TestItem(id=1, name="Item 1")]

        paginated = PaginatedSchema[TestItem](
            count=1,
            items=items,
            next_page=2,
            previous_page=None,
            total_pages=5,
            per_page=10,
            current_page=1,
        )

        serialized = paginated.model_dump()

        expected_keys = {
            "count",
            "items",
            "next_page",
            "previous_page",
            "total_pages",
            "per_page",
            "current_page",
        }
        self.assertEqual(set(serialized.keys()), expected_keys)
        self.assertEqual(serialized["count"], 1)
        self.assertEqual(len(serialized["items"]), 1)
        self.assertEqual(serialized["items"][0]["id"], 1)

    def test_paginated_schema_generic_type(self):
        """Test PaginatedSchema works with different generic types."""
        # Test with string items
        string_paginated = PaginatedSchema[str](
            count=2,
            items=["item1", "item2"],
            next_page=None,
            previous_page=None,
            total_pages=1,
            per_page=10,
            current_page=1,
        )

        self.assertEqual(string_paginated.items[0], "item1")
        self.assertEqual(string_paginated.items[1], "item2")

        # Test with integer items
        int_paginated = PaginatedSchema[int](
            count=3,
            items=[1, 2, 3],
            next_page=None,
            previous_page=None,
            total_pages=1,
            per_page=10,
            current_page=1,
        )

        self.assertEqual(int_paginated.items[0], 1)
        self.assertEqual(int_paginated.items[2], 3)


if __name__ == "__main__":
    unittest.main()
