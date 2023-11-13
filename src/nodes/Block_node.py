from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable):
        for child in self.children:
            value = child.evaluate(context)

            if isinstance(child, nodes.Return):
                return value

        return Typed_value.NULL
