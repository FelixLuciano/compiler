from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Integer_value_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable, program: Program):
        program.write(f"MOV EAX, {self.value}")

        return Typed_value(
            type=Typed_value.types.INT,
            value=int(self.value)
        )
