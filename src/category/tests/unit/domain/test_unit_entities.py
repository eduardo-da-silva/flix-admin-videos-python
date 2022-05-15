from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import unittest
from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):  # sourcery skip: extract-duplicate-method
        category = Category(name="Movie")
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
        category1 = Category(name="Movie 1")
        category2 = Category(name="Movie 2")
        self.assertNotEqual(category1.created_at, category2.created_at)

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            category = Category(name="test")
            category.name = "test 2"

    def test_if_update_a_category_name(self):
        category1 = Category(name="Movie name", description="Movie description")
        category1.update(name="Movie name updated")
        self.assertEqual(category1.name, "Movie name updated")
        self.assertEqual(category1.description, "Movie description")

    def test_if_update_a_category_description(self):
        category1 = Category(name="Movie name", description="Movie description")
        category1.update(description="Movie description updated")
        self.assertEqual(category1.name, "Movie name")
        self.assertEqual(category1.description, "Movie description updated")

    def test_if_update_a_category_name_and_description(self):
        category1 = Category(name="Movie name", description="Movie description")
        category1.update(
            name="Movie name updated", description="Movie description updated"
        )
        self.assertEqual(category1.name, "Movie name updated")
        self.assertEqual(category1.description, "Movie description updated")

    def test_if_a_category_is_activated(self):
        category1 = Category(name="Movie name")
        category1.activate()
        self.assertTrue(category1.is_active)

    def test_if_a_category_is_deactivated(self):
        category1 = Category(name="Movie name")
        category1.deactivate()
        self.assertFalse(category1.is_active)

    def test_if_a_category_is_activated_after_deactivate(self):
        category1 = Category(name="Movie name")
        category1.deactivate()
        self.assertFalse(category1.is_active)
        category1.activate()
        self.assertTrue(category1.is_active)
