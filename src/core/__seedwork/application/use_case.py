from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class UseCase(Generic[Input, Output], ABC):  # pylint: disable=too-few-public-methods

    @abstractmethod
    def execute(self, input_param: Input) -> Output:
        raise NotImplementedError()
