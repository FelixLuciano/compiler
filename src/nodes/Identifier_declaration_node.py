import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Identifier_declaration_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable, program: Program):
        type_str = self.children[0].value

        if type_str == "int":
            type_ = Typed_value.types.INT
        elif type_str == "string":
            type_ = Typed_value.types.STRING
        else:
            raise TypeError(f"{type_str} is not an valid type!")

        context.declare(self.value, type_)
        program.write(f"PUSH DWORD 0 ; var {self.value} {type_str} [EBP-{SymbolTable.stack_pointer}]")

        if len(self.children) > 1:
            return self.children[1].evaluate(context, program)

        return Typed_value.NULL
