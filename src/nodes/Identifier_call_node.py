from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Identifier_call_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable):
        func = context.get(self.value)
        args = (child.evaluate(context) for child in self.children)

        if func.type == Typed_value.types.FUNCTION:
            if callable(func.value):
                return func.value(*args)

        raise ValueError(f"{self.value} is not a function!")
