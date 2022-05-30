from dataclasses import asdict, dataclass
from typing import Optional
from __seedwork.application.dto import PaginationOutput, PaginationOutputMapper, SearchInput
from __seedwork.application.use_case import UseCase
from category.application.dto import CategoryOutput, CategoryOutputMapper

from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCase):

    category_repository: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = Category(  # pylint: disable=unexpected-keyword-arg
            name=input_param.name,
            description=input_param.description,
            is_active=input_param.is_active
        )
        self.category_repository.insert(category)
        return CategoryOutputMapper.from_child(CreateCategoryUseCase.Output).to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    category_repository: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = self.category_repository.find_by_id(input_param.id)
        return CategoryOutputMapper.from_child(GetCategoryUseCase.Output).to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str         # pylint: disable=invalid-name

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCase):
    category_repository: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        search_params = self.category_repository.SearchParams(**asdict(input_param))
        result = self.category_repository.search(search_params)
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepository.SearchResult):     # pylint: disable=no-self-use
        items = list(map(CategoryOutputMapper.without_child().to_output, result.items))
        return PaginationOutputMapper.from_child(ListCategoriesUseCase.Output).to_output(items, result)

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(UseCase):

    category_repository: CategoryRepository

    def execute(self, input_param: 'Input') -> None:
        self.category_repository.delete(input_param.id)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str         # pylint: disable=invalid-name


@dataclass(slots=True, frozen=True)
class UpdateCategoryUseCase(UseCase):

    category_repository: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        entity = self.category_repository.find_by_id(input_param.id)
        entity.update(name=input_param.name, description=input_param.description)
        if input_param.is_active is True:
            entity.activate()
        if input_param.is_active is False:
            entity.deactivate()
        self.category_repository.update(entity)
        return CategoryOutputMapper.from_child(UpdateCategoryUseCase.Output).to_output(entity)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str         # pylint: disable=invalid-name
        name: str
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass
