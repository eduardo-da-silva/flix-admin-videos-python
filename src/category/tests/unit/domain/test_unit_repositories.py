import typing
from __seedwork.domain.value_objects import UniqueEntityId
from dataclasses import dataclass
from typing import Optional, List
import unittest
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

from __seedwork.domain.repositories import (T, Filter, InMemoryRepository, InMemorySearchableRepository,
                                            RepositoryInterface, SearchParams, SearchResult,
                                            SearchableRepositoryInterface)


class TestRepositoryInterfaceUnit(unittest.TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class RepositoryInterface with abstract methods " +
                         "delete, find_all, find_by_id, insert, update")


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepositoryUnit(unittest.TestCase):
    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert_item(self):
        entity = StubEntity(name="teste", price=5)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw__not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake_id')
        self.assertEqual(assert_error.exception.args[0], "Entity not found using id 'fake_id'")

        unique_entity_id = UniqueEntityId('8e65b539-6bdb-42eb-b782-1470846e9cbf')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(assert_error.exception.args[0],
                         "Entity not found using id '8e65b539-6bdb-42eb-b782-1470846e9cbf'")

    def test_find_by_id(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)

        entities = self.repo.find_all()
        self.assertListEqual(entities, [entity])

    def test_throw__not_found_exception_in_update(self):
        entity = StubEntity(name='test', price=10)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(assert_error.exception.args[0], f"Entity not found using id '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(assert_error.exception.args[0],
                         f"Entity not found using id '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name='test', price=10)
        self.repo.insert(entity)

        entity_updated = StubEntity(unique_entity_id=entity.unique_entity_id, name='updated', price=5)
        self.repo.update(entity_updated)
        self.assertEqual(entity_updated, self.repo.items[0])

    def test_throw__not_found_exception_in_delete(self):
        entity = StubEntity(name='test', price=10)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        self.assertEqual(assert_error.exception.args[0], f"Entity not found using id '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.unique_entity_id)
        self.assertEqual(assert_error.exception.args[0],
                         f"Entity not found using id '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name='test', price=10)
        self.repo.insert(entity)
        self.repo.delete(entity.id)
        self.assertEqual(self.repo.items, [])

        self.repo.insert(entity)
        self.repo.delete(entity.unique_entity_id)
        self.assertEqual(self.repo.items, [])


class TestSearchableRepositoryInterfaceUnit(unittest.TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class SearchableRepositoryInterface with abstract methods " +
                         "delete, find_all, find_by_id, insert, search, update")


class TestSearchParamsUnit(unittest.TestCase):
    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': typing.Optional[int],
            'per_page': typing.Optional[int],
            'sort': typing.Optional[str],
            'sort_dir': typing.Optional[str],
            'filter': typing.Optional[Filter]})

    def test_page_prop(self):
        params = SearchParams()

        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': '1', 'expected': 1},
            {'page': '', 'expected': 1},
            {'page': True, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 5, 'expected': 5},
            {'page': 5.5, 'expected': 5},
        ]

        for item in arrange:
            params = SearchParams(page=item['page'])
            self.assertEqual(params.page, item['expected'])

    def test_per_page_prop(self):
        params = SearchParams()

        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': '', 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 5, 'expected': 5},
            {'per_page': 1, 'expected': 1},
            {'per_page': '1', 'expected': 1},
            {'per_page': 'fake', 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': 25, 'expected': 25},
        ]

        for item in arrange:
            params = SearchParams(per_page=item['per_page'])
            self.assertEqual(params.per_page, item['expected'])

    def test_sort_prop(self):
        params = SearchParams()

        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': '', 'expected': None},
            {'sort': 0, 'expected': '0'},
            {'sort': {}, 'expected': '{}'},
            {'sort': 5.5, 'expected': '5.5'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': 'False'},
        ]

        for item in arrange:
            params = SearchParams(sort=item['sort'])
            self.assertEqual(params.sort, item['expected'])

    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)
        params = SearchParams(sort="")
        self.assertIsNone(params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': 'asc'},
            {'sort_dir': '', 'expected': 'asc'},
            {'sort_dir': 0, 'expected': 'asc'},
            {'sort_dir': {}, 'expected': 'asc'},
            {'sort_dir': 5.5, 'expected': 'asc'},
            {'sort_dir': True, 'expected': 'asc'},
            {'sort_dir': False, 'expected': 'asc'},
            {'sort_dir': 'asc', 'expected': 'asc'},
            {'sort_dir': 'ASC', 'expected': 'asc'},
            {'sort_dir': 'desc', 'expected': 'desc'},
            {'sort_dir': 'DESC', 'expected': 'desc'},
        ]

        for item in arrange:
            params = SearchParams(sort='name', sort_dir=item['sort_dir'])
            self.assertEqual(params.sort_dir, item['expected'])

    def test_filter_prop(self):
        params = SearchParams()

        self.assertIsNone(params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': '', 'expected': None},
            {'filter': 0, 'expected': '0'},
            {'filter': {}, 'expected': '{}'},
            {'filter': 5.5, 'expected': '5.5'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
        ]

        for item in arrange:
            params = SearchParams(filter=item['filter'])
            self.assertEqual(params.filter, item['expected'])


class TestSearchResultUnit(unittest.TestCase):
    def test_props_annotations(self):
        self.assertEqual(SearchResult.__annotations__, {
            'items': List[T],
            'total': int,
            'current_page': int,
            'per_page': int,
            'last_page': int,
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter],
        })

    def test_constructor(self):
        entity = StubEntity(name='fake', price=5)
        result = SearchResult(items=[entity, entity], total=4, current_page=1, per_page=2)
        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None,
        })

        result = SearchResult(
            items=[entity, entity],
            total=5,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='test'
        )
        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 5,
            'current_page': 1,
            'per_page': 2,
            'last_page': 3,
            'sort': 'name',
            'sort_dir': 'asc',
            'filter': 'test',
        })

    def test_when_per_page_is_greater_than_total(self):
        result = SearchResult(
            items=[],
            total=5,
            current_page=1,
            per_page=15
        )
        self.assertEqual(result.last_page, 1)

    def test_when_per_page_is_less_than_total_and_they_are_not_multiple(self):
        result = SearchResult(
            items=[],
            total=31,
            current_page=1,
            per_page=15
        )
        self.assertEqual(result.last_page, 3)


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ['name']

    def _apply_filter(self, items: List[StubEntity], filter_param: str | None) -> List[StubEntity]:
        if(filter_param):
            filter_obj = filter(lambda item: filter_param.lower() in item.name.lower()
                                or filter_param == str(item.price), items)
            return list(filter_obj)
        return items


class TestInMemorySearchableRepositoryUnit(unittest.TestCase):

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        items = [StubEntity(name='test', price=5)]
        result = self.repo._apply_filter(items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name='test', price=5),
            StubEntity(name='TEST', price=5),
            StubEntity(name='fake', price=6),
        ]

        result = self.repo._apply_filter(items, 'Test')
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_filter(items, '5')
        self.assertEqual([items[0], items[1]], result)

    def test__apply_sort(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=0),
            StubEntity(name='c', price=2)
        ]

        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual(items, result)

        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual([items[2], items[0], items[1]], result)

        self.repo.sortable_fields.append('price')

        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(items, 'price', 'desc')
        self.assertEqual([items[2], items[0], items[1]], result)

    def test__apply_paginate(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=0),
            StubEntity(name='c', price=2),
            StubEntity(name='d', price=2),
            StubEntity(name='e', price=2)
        ]

        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual([items[2], items[3]], result)

        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual([items[4]], result)

        result = self.repo._apply_paginate(items, 4, 2)
        self.assertEqual([], result)

    def test_search_when_params_is_empty(self):
        entity = StubEntity(name='b', price=1)
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
            sort_dir=None,
            sort=None,
            filter=None
        ))

    def test_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='TeST', price=1),
        ]

        self.repo.items = items

        result = self.repo.search(SearchParams(page=1, per_page=2, filter='TEST'))
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
            sort_dir=None,
            sort=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(page=2, per_page=2, filter='TEST'))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
            sort_dir=None,
            sort=None,
            filter='TEST'
        ))

    def test_search_applying_sort_and_paginate(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='c', price=1),
        ]

        self.repo.items = items

        result = self.repo.search(SearchParams(page=1, per_page=2, sort='name'))
        self.assertEqual(result, SearchResult(
            items=[items[1], items[0]],
            total=5,
            current_page=1,
            per_page=2,
            sort_dir='asc',
            sort='name',
            filter=None
        ))

        result = self.repo.search(SearchParams(page=2, per_page=2, sort='name'))
        self.assertEqual(result, SearchResult(
            items=[items[4], items[2]],
            total=5,
            current_page=2,
            per_page=2,
            sort_dir='asc',
            sort='name',
            filter=None
        ))

        result = self.repo.search(SearchParams(page=3, per_page=2, sort='name'))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=5,
            current_page=3,
            per_page=2,
            sort_dir='asc',
            sort='name',
            filter=None
        ))

        result = self.repo.search(SearchParams(page=1, per_page=2, sort='name', sort_dir='desc'))
        self.assertEqual(result, SearchResult(
            items=[items[3], items[2]],
            total=5,
            current_page=1,
            per_page=2,
            sort_dir='desc',
            sort='name',
            filter=None
        ))
