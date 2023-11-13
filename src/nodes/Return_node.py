from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Return_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable) -> Typed_value:
        return self.children[0].evaluate(context)
