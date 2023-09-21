import typing as T
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from src.SymbolTable import SymbolTable


@dataclass
class Abstract_node(ABC):
    value: T.Any = field()
    children: T.List["Abstract_node"] = field(default_factory=list)

    @abstractmethod
    def evaluate(self, context: SymbolTable) -> int:
        pass
