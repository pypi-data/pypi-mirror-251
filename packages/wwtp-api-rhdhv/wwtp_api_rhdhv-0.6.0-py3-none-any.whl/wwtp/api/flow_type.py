from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Union, Annotated


@dataclass
class FlowType(ABC):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


T = TypeVar("T", bound=Union[FlowType])
UseInputAsOutput = Annotated[T, "UseInputAsOutput"]
