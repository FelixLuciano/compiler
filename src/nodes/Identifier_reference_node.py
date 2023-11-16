import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable
from src.Program import Program


@dataclass
class Identifier_reference_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable, program: Program):
        value, pointer = context.get(self.value)

        program.write(f"MOV EAX, [EBP-{pointer+4}] ; Recupera valor de {self.value}")

        return value
