from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable, program: Program):
        for child in self.children:
            child.evaluate(context, program)

        return Typed_value.NULL
