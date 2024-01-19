from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic

T = TypeVar("T", bound=Enum)


class Toggleable(Generic[T], ABC):

    @classmethod
    @abstractmethod
    def type(cls) -> T | list[T]:
        pass
