from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Iterator_block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable):
        assignment, condition, step, block = self.children

        assignment.evaluate(context)
        while Typed_value.is_true(condition.evaluate(context)):
            block.evaluate(context)
            step.evaluate(context)

        return Typed_value.NULL
