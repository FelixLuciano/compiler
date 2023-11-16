import typing as T
from dataclasses import dataclass, field

from src.Token import Token
import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Binary_operation_node(nodes.Node):
    value: Token.types = field()

    OPERATIONS: T.Dict[Token.types, T.Callable[[T.Any, T.Any], T.Any]] = field(init=False, repr=False)

    def evaluate(self, context: SymbolTable, program: Program):
        a, b = self.children
        y = b.evaluate(context, program)

        program.write("PUSH EAX")

        x = a.evaluate(context, program)

        program.write("POP EBX")

        if self.value == Token.types.OP_PLUS:
            program.write("ADD EAX, EBX")
        elif self.value == Token.types.OP_MINUS:
            program.write("SUB EAX, EBX")
        elif self.value == Token.types.OP_MULT:
            program.write("IMUL EAX, EBX")
        elif self.value == Token.types.OP_DIV:
            program.write("IDIV EBX")

        elif self.value == Token.types.OP_EQUAL:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_je",
            )
        elif self.value == Token.types.OP_NOT_EQUAL:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_je",
            )
        elif self.value == Token.types.OP_GREATER:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_jg",
            )
        elif self.value == Token.types.OP_GREATER_EQUAL:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_jl",
                "CMP EAX, False",
            )
        elif self.value == Token.types.OP_LOWER:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_jl",
            )
        elif self.value == Token.types.OP_LOWER_EQUAL:
            program.write(
                "CMP EAX, EBX",
                "CALL binop_jg",
                "CMP EAX, False",
            )

        try:
            method = Binary_operation_node.OPERATIONS[self.value]

            if x.type != y.type:
                if self.value != Token.types.OP_CONCAT:
                    raise TypeError(f"Invalid operation {self.value.name} between {x.type.name} and {y.type.name}")

            return Typed_value(
                type=x.type,
                value=method(x.value, y.value),
            )
        except KeyError:
            raise ValueError(f"{self.value} is not an Valid operation!")


Binary_operation_node.OPERATIONS = {
    Token.types.OP_PLUS: lambda x, y: x + y,
    Token.types.OP_MINUS: lambda x, y: x - y,
    Token.types.OP_MULT: lambda x, y: x * y,
    Token.types.OP_DIV: lambda x, y: x // y,
    Token.types.OP_MODULO: lambda x, y: x % y,
    # Token.types.OP_POWER: lambda x, y: x ** y,
    Token.types.OP_CONCAT: lambda x, y: "".join(map(str, [x, y])),
    Token.types.OP_AND: lambda x, y: 1 if x and y else 0,
    Token.types.OP_OR: lambda x, y: 1 if x or y else 0,
    Token.types.OP_EQUAL: lambda x, y: 1 if x == y else 0,
    Token.types.OP_NOT_EQUAL: lambda x, y: 1 if x != y else 0,
    Token.types.OP_GREATER: lambda x, y: 1 if x > y else 0,
    Token.types.OP_LOWER: lambda x, y: 1 if x < y else 0,
    Token.types.OP_GREATER_EQUAL: lambda x, y: 1 if x >= y else 0,
    Token.types.OP_LOWER_EQUAL: lambda x, y: 1 if x <= y else 0,
}
