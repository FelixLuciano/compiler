from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class String_value_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable) -> Typed_value:
        return Typed_value(
            type=Typed_value.types.STRING,
            value=self.value
        )
