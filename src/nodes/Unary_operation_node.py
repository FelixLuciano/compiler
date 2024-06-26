import math
import typing as T
from dataclasses import dataclass, field

import src.nodes as nodes
from src.Token import Token
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


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

    def evaluate(self, context: SymbolTable, program: Program):
        x = self.children[0].evaluate(context, program)

        if x.type != Typed_value.types.INT:
            raise ValueError(f"Invalid unary operation {self.value.name} for type {x.type.name}")
        
        if self.value == Token.types.OP_MINUS:
            program.write(
                "NEG EAX",
            )
        elif self.value == Token.types.OP_NOT:
            program.write(
                "NOT EAX",
            )

        try:
            method = Unary_operation_node.OPERATIONS[self.value]
            
            return Typed_value(
                type=x.type,
                value=method(x.value),
            )
        except KeyError:
            raise ValueError(f"{self.value} is not an Valid operation!")


Unary_operation_node.OPERATIONS = {
    Token.types.OP_PLUS: lambda x: x,
    Token.types.OP_MINUS: lambda x: -x,
    Token.types.OP_NOT: lambda x: 0 if x == 1 else 1,
    Token.types.OP_FATORIAL: lambda x: math.factorial(x),
}
