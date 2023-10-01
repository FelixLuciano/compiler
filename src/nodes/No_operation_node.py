from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable


@dataclass
class No_operation_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable) -> None:
        return None
