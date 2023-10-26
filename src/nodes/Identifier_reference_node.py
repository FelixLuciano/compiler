import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable


@dataclass
class Identifier_reference_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable):
        return context.get(self.value)
