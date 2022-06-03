from datetime import datetime, timedelta
from typing import Optional
import unittest
from unittest.mock import patch
from core.__seedwork.application.dto import PaginationOutput, SearchInput
from core.__seedwork.application.use_case import UseCase
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.application.dto import CategoryOutput, CategoryOutputMapper
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    DeleteCategoryUseCase,
    UpdateCategoryUseCase,
)
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository


from core.category.infra.in_memory.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):

    use_case: CreateCategoryUseCase
    category_repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repository = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repository)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__, {
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool]
        })

        description_field = CreateCategoryUseCase.Input.__dataclass_fields__[       # pylint: disable=no-member
            'description']
        self.assertEqual(description_field.default, Category.get_field('description').default)

        is_active_field = CreateCategoryUseCase.Input.__dataclass_fields__['is_active']  # pylint: disable=no-member
        self.assertEqual(is_active_field.default, Category.get_field('is_active').default)

    def test_output(self):
        self.assertTrue(issubclass(CreateCategoryUseCase.Output, CategoryOutput))

    def test_execute(self):
        with patch.object(self.category_repository, 'insert', wraps=self.category_repository.insert) as spy_insert:
            input_param = CreateCategoryUseCase.Input(
                name='Movie',
                description='Movie description',
                is_active=True
            )
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output.name, 'Movie')
            self.assertEqual(output.description, 'Movie description')
            self.assertEqual(output.is_active, True)
            self.assertIsNotNone(output.id)
            self.assertIsNotNone(output.created_at)

            input_param = CreateCategoryUseCase.Input(
                name='Movie 2',
                description=None,
                is_active=False
            )
            output = self.use_case.execute(input_param)
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repository.items[1].id,
                name="Movie 2",
                description=None,
                is_active=False,
                created_at=self.category_repository.items[1].created_at
            ))

            input_param = CreateCategoryUseCase.Input(
                name='Movie 3'
            )
            output = self.use_case.execute(input_param)
            print(output)
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repository.items[2].id,
                name="Movie 3",
                description=None,
                is_active=True,
                created_at=self.category_repository.items[2].created_at
            ))


class TestGetCategoryUseCaseUnit(unittest.TestCase):

    use_case: GetCategoryUseCase
    category_repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repository = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repository)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(GetCategoryUseCase.Input.__annotations__, {
            'id': str,
        })

    def test_throw_exception_when_category_not_found(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        with patch.object(
            self.category_repository, 'find_by_id', wraps=self.category_repository.find_by_id
        ) as spy_find_by_id:
            input_param = GetCategoryUseCase.Input('fake_id')
            with self.assertRaises(NotFoundException) as assert_error:
                self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], "Entity not found using id 'fake_id'")

    def test_output(self):
        self.assertTrue(issubclass(GetCategoryUseCase.Output, CategoryOutput))

    def test_execute(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        with patch.object(
            self.category_repository, 'find_by_id', wraps=self.category_repository.find_by_id
        ) as spy_find_by_id:
            input_param = GetCategoryUseCase.Input(category.id)
            output = self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            self.assertEqual(output, GetCategoryUseCase.Output(
                id=self.category_repository.items[0].id,
                name='Movie',
                description='Movie description',
                is_active=True,
                created_at=self.category_repository.items[0].created_at
            ))


class TestListCategoryUseCaseUnit(unittest.TestCase):

    use_case: ListCategoriesUseCase
    category_repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repository = CategoryInMemoryRepository()
        self.use_case = ListCategoriesUseCase(self.category_repository)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertTrue(issubclass(ListCategoriesUseCase.Input, SearchInput))

    def test_output(self):
        self.assertTrue(issubclass(ListCategoriesUseCase.Output, PaginationOutput))

    def test__to_output(self):
        entity = Category(name="Movie")
        default_props = {
            'total': 1,
            'current_page': 1,
            'per_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None
        }
        result = CategoryRepository.SearchResult(items=[], **default_props)
        output = self.use_case._ListCategoriesUseCase__to_output(result)        # pylint: disable=protected-access
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=[],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        ))

        result = CategoryRepository.SearchResult(items=[entity], **default_props)
        output = self.use_case._ListCategoriesUseCase__to_output(result)    # pylint: disable=protected-access
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=[CategoryOutput(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
                created_at=entity.created_at
            )],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        ))

    def test_execute_using_empty_search_params(self):
        self.category_repository.items = [
            Category(name="Movie 1"),
            Category(name="Movie 2", created_at=datetime.now() + timedelta(seconds=200)),
        ]

        with patch.object(self.category_repository, 'search', wraps=self.category_repository.search) as spy_search:
            input_param = ListCategoriesUseCase.Input()
            output = self.use_case.execute(input_param)
            spy_search.assert_called_once()
            self.assertEqual(output, ListCategoriesUseCase.Output(
                items=list(map(CategoryOutputMapper.without_child().to_output, self.category_repository.items[::-1])),
                total=2,
                current_page=1,
                per_page=15,
                last_page=1
            ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        items = [
            Category(name="a"),
            Category(name="AAA"),
            Category(name="AaA"),
            Category(name="b"),
            Category(name="c"),
        ]
        self.category_repository.items = items

        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(map(CategoryOutputMapper.without_child().to_output, [items[1], items[2]])),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(map(CategoryOutputMapper.without_child().to_output, [items[0]])),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(map(CategoryOutputMapper.without_child().to_output, [items[0], items[2]])),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(map(CategoryOutputMapper.without_child().to_output, [items[1]])),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))


class TestDeleteCategoryUseCaseUnit(unittest.TestCase):

    use_case: DeleteCategoryUseCase
    category_repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repository = CategoryInMemoryRepository()
        self.use_case = DeleteCategoryUseCase(self.category_repository)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(DeleteCategoryUseCase.Input.__annotations__, {
            'id': str,
        })

    def test_throw_exception_when_category_not_found(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        with patch.object(
            self.category_repository, 'delete', wraps=self.category_repository.delete
        ) as spy_delete:
            input_param = DeleteCategoryUseCase.Input('fake_id')
            with self.assertRaises(NotFoundException) as assert_error:
                self.use_case.execute(input_param)
            spy_delete.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], "Entity not found using id 'fake_id'")

    def test_execute(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        with patch.object(
            self.category_repository, 'delete', wraps=self.category_repository.delete
        ) as spy_delete:
            input_param = DeleteCategoryUseCase.Input(category.id)
            self.use_case.execute(input_param)
            spy_delete.assert_called_once()
            self.assertEqual(self.category_repository.items, [])


class TestUpdateCategoryUseCaseUnit(unittest.TestCase):
    use_case: UpdateCategoryUseCase
    category_repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repository = CategoryInMemoryRepository()
        self.use_case = UpdateCategoryUseCase(self.category_repository)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(UpdateCategoryUseCase.Input.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool]
        })

        description_field = UpdateCategoryUseCase.Input.__dataclass_fields__[       # pylint: disable=no-member
            'description']
        self.assertEqual(description_field.default, Category.get_field('description').default)

        is_active_field = UpdateCategoryUseCase.Input.__dataclass_fields__['is_active']  # pylint: disable=no-member
        self.assertEqual(is_active_field.default, Category.get_field('is_active').default)

    def test_output(self):
        self.assertTrue(issubclass(UpdateCategoryUseCase.Output, CategoryOutput))

    def test_throw_exception_when_category_not_found(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        input_param = UpdateCategoryUseCase.Input(
            id='fake_id',
            name='Movie updated',
            description='Movie description updated',
            is_active=False
        )
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(assert_error.exception.args[0], "Entity not found using id 'fake_id'")

    def test_execute(self):
        category = Category(name='Movie', description='Movie description', is_active=True)
        self.category_repository.items = [category]
        with patch.object(self.category_repository, 'update', wraps=self.category_repository.update) as spy_update:
            input_param = UpdateCategoryUseCase.Input(
                id=category.id,
                name='Movie updated',
                description='Movie description updated',
                is_active=False
            )
            output = self.use_case.execute(input_param)
            spy_update.assert_called_once()
            self.assertEqual(output.name, 'Movie updated')
            self.assertEqual(output.description, 'Movie description updated')
            self.assertEqual(output.is_active, False)
            self.assertEqual(output.id, category.id)
            self.assertIsNotNone(output.created_at)

            # input_param = UpdateCategoryUseCase.Input(
            #     name='Movie 2',
            #     description=None,
            #     is_active=False
            # )
            # output = self.use_case.execute(input_param)
            # self.assertEqual(output, UpdateCategoryUseCase.Output(
            #     id=self.category_repository.items[1].id,
            #     name="Movie 2",
            #     description=None,
            #     is_active=False,
            #     created_at=self.category_repository.items[1].created_at
            # ))

            # input_param = UpdateCategoryUseCase.Input(
            #     name='Movie 3'
            # )
            # output = self.use_case.execute(input_param)
            # print(output)
            # self.assertEqual(output, UpdateCategoryUseCase.Output(
            #     id=self.category_repository.items[2].id,
            #     name="Movie 3",
            #     description=None,
            #     is_active=True,
            #     created_at=self.category_repository.items[2].created_at
            # ))
