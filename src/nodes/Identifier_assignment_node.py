from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable
from src.Program import Program


@dataclass
class Identifier_assignment_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable, program: Program):
        old_value, pointer = context.get(self.value)
        value = self.children[0].evaluate(context, program)

        context.set(self.value, value)
        program.write(f"MOV [EBP-{pointer + 4}], EAX ; {self.value} = ...")

        return value
