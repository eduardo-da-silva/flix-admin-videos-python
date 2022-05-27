from datetime import datetime, timedelta
import unittest

from category.domain.entities import Category

from category.infra.repositories import CategoryInMemoryRepository


class TestCategoryInMemoryRepository(unittest.TestCase):
    repo: CategoryInMemoryRepository

    def setUp(self):
        self.repo = CategoryInMemoryRepository()

    def test_if_no_filter_when_filter_params_is_null(self):
        entity = Category(name='Movie')
        items = [entity]

        filtered_items = self.repo._apply_filter(items, None)
        self.assertEqual(filtered_items, items)

    def test_filter(self):
        items = [
            Category(name='test'),
            Category(name='TEST'),
            Category(name='fake')
        ]

        filtered_items = self.repo._apply_filter(items, 'TEST')
        self.assertEqual(filtered_items, [items[0], items[1]])

    def test_sort_by_created_at_when_sort_param_is_null(self):
        items = [
            Category(name='test'),
            Category(name='TEST', created_at=datetime.now() + timedelta(seconds=100)),
            Category(name='fake', created_at=datetime.now() + timedelta(seconds=200))
        ]

        sorted_items = self.repo._apply_sort(items, None, None)
        self.assertListEqual(sorted_items, [items[2], items[1], items[0]])

    def test_sort_name(self):
        items = [
            Category(name='c'),
            Category(name='a'),
            Category(name='b')
        ]

        sorted_items = self.repo._apply_sort(items, 'name', 'asc')
        self.assertListEqual(sorted_items, [items[1], items[2], items[0]])
