from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable


@dataclass
class Identifier_assignment_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable):
        value = self.children[0].evaluate(context)

        context.set(self.value, value)

        return value
