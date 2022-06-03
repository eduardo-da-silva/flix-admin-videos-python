from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import typing
import unittest
from unittest.mock import patch
from core.category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_if_annotations_is_valid(self):
        self.assertEqual(Category.__annotations__, {
            'name': str,
            'description': typing.Optional[str],
            'is_active': typing.Optional[bool],
            'created_at': typing.Optional[datetime]})

    def test_constructor(self):  # sourcery skip: extract-duplicate-method
        with patch.object(Category, "validate") as mock_validate_method:
            category = Category(name="Movie")
            mock_validate_method.assert_called_once()
            self.assertEqual(category.name, "Movie")
            self.assertEqual(category.description, None)
            self.assertEqual(category.is_active, True)
            self.assertIsInstance(category.created_at, datetime)

            created_at = datetime.now()
            category = Category(
                name="Movie",
                description="Movie description",
                is_active=False,
                created_at=created_at,
            )
            self.assertEqual(category.name, "Movie")
            self.assertEqual(category.description, "Movie description")
            self.assertEqual(category.is_active, False)
            self.assertEqual(category.created_at, created_at)

    def test_if_created_at_is_generated_in_constructor(self):
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie 1")
            category2 = Category(name="Movie 2")
            self.assertNotEqual(category1.created_at, category2.created_at)

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            with patch.object(Category, "validate"):
                category = Category(name="test")
                category.name = "test 2"

    def test_if_update_a_category_name_and_description(self):
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie name", description="Movie description")
            category1.update(
                name="Movie name updated", description="Movie description updated"
            )
            self.assertEqual(category1.name, "Movie name updated")
            self.assertEqual(category1.description, "Movie description updated")

    def test_if_a_category_is_activated(self):
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie name")
            category1.activate()
            self.assertTrue(category1.is_active)

    def test_if_a_category_is_deactivated(self):
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie name")
            category1.deactivate()
            self.assertFalse(category1.is_active)

    def test_if_a_category_is_activated_after_deactivate(self):
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie name")
            category1.deactivate()
            self.assertFalse(category1.is_active)
            category1.activate()
            self.assertTrue(category1.is_active)
