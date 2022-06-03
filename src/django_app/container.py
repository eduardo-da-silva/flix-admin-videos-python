from dependency_injector import containers, providers

from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase


class Container(containers.DeclarativeContainer):

    repository_category_in_memory = providers.Singleton(CategoryInMemoryRepository)

    use_case_category_create_category = providers.Singleton(
        CreateCategoryUseCase, category_repository=repository_category_in_memory)

    use_case_category_list_categories = providers.Singleton(
        ListCategoriesUseCase, category_repository=repository_category_in_memory)
