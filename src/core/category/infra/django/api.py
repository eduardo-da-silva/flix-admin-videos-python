from dataclasses import asdict, dataclass
from typing import Callable

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository


# class CreateCategoryUseCseFactory:
#     @staticmethod
#     def create():
#         return Create


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]

    def get(self, request: Request) -> Response:
        input_params = ListCategoriesUseCase.Input()
        output = self.list_use_case().execute(input_params)
        return Response(asdict(output))

    def post(self, request: Request) -> Response:
        # create_use_case = CreateCategoryUseCase(self.repo)
        input_params = CreateCategoryUseCase.Input(name=request.data['name'])
        output = self.create_use_case().execute(input_params)
        return Response(asdict(output))

    def test(self):
        x = 10
        if x == 10:
            return True
        if x == 20:
            return False
