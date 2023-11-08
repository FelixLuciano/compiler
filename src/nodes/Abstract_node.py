import typing as T
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Abstract_node(ABC):
    value: T.Any = field()
    children: T.List["Abstract_node"] = field(default_factory=list)
    id: int = field(default_factory=lambda: Abstract_node.new_id())

    i: int = 0

    @staticmethod
    def new_id():
        Abstract_node.i += 1

        return Abstract_node.i

    @abstractmethod
    def evaluate(self, context: SymbolTable) -> Typed_value:
        pass
