import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value


@dataclass
class Identifier_declaration_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable):
        type_str = self.children[0].value

        if type_str == "int":
            type_ = Typed_value.types.INT
        elif type_str == "string":
            type_ = Typed_value.types.STRING
        else:
            raise TypeError(f"{type_str} is not an valid type!")

        context.declare(self.value, type_)

        if len(self.children) > 1:
            return self.children[1].evaluate(context)

        return Typed_value.NULL
