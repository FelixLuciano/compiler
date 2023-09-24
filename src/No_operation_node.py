from dataclasses import dataclass, field

from src.Abstract_node import Abstract_node
from src.SymbolTable import SymbolTable


@dataclass
class No_operation_node(Abstract_node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable) -> None:
        return None
