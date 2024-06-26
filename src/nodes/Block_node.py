from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable, program: Program):
        program.indent()

        for child in self.children:
            value = child.evaluate(context, program)

            if isinstance(child, nodes.Return):
                return value

        program.unindent()

        return Typed_value.NULL
