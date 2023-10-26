from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Conditional_block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable):
        value: Typed_value = self.children[0].evaluate(context)

        if Typed_value.is_true(value):
            self.children[1].evaluate(context)
        elif (len(self.children) > 2):
            self.children[2].evaluate(context)

        return Typed_value.NULL
