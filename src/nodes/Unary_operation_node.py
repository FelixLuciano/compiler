import math
import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Token import Token


@dataclass
class Unary_operation_node(nodes.Node):
    value: Token.types = field()

    OPERATIONS: T.Dict[Token.types, T.Callable[[T.Any], T.Any]] = field(
        init=False,
        repr=False,
        default_factory=lambda: {
            Token.types.OP_PLUS: lambda x: x,
            Token.types.OP_MINUS: lambda x: -x,
            Token.types.OP_NOT: lambda x: 0 if x == 1 else 1,
            Token.types.OP_FATORIAL: lambda x: math.factorial(x),
        }
    )

    def evaluate(self, context: SymbolTable):
        x = self.children[0].evaluate(context)

        if x.type != Typed_value.types.INT:
            raise Exception(f"Invalid unary operation into type {x.type.name}")

        try:
            method = Unary_operation_node.OPERATIONS[self.value]
            
            return method(x)
        except KeyError:
            raise ValueError(f"{self.value} is not an Valid operation!")


Unary_operation_node.OPERATIONS = {
    Token.types.OP_PLUS: lambda x: x,
    Token.types.OP_MINUS: lambda x: -x,
    Token.types.OP_NOT: lambda x: 0 if x == 1 else 1,
    Token.types.OP_FATORIAL: lambda x: math.factorial(x),
}
