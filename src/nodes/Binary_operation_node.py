import src.nodes as nodes
from src.SymbolTable import SymbolTable
from src.Token import Token


class Binary_operation_node(nodes.Node):
    value: Token.types

    OPERATIONS = {
        Token.types.OP_PLUS: lambda x, y: x + y,
        Token.types.OP_MINUS: lambda x, y: x - y,
        Token.types.OP_MULT: lambda x, y: x * y,
        Token.types.OP_DIV: lambda x, y: x // y,
        # Token.types.OP_POWER: lambda x, y: x ** y,
        Token.types.OP_AND: lambda x, y: 1 if x and y else 0,
        Token.types.OP_OR: lambda x, y: 1 if x or y else 0,
        Token.types.OP_EQUAL: lambda x, y: 1 if x == y else 0,
        Token.types.OP_NOT_EQUAL: lambda x, y: 1 if x != y else 0,
        Token.types.OP_GREATER: lambda x, y: 1 if x > y else 0,
        Token.types.OP_LOWER: lambda x, y: 1 if x < y else 0,
        Token.types.OP_GREATER_EQUAL: lambda x, y: 1 if x >= y else 0,
        Token.types.OP_LOWER_EQUAL: lambda x, y: 1 if x <= y else 0,
    }

    def evaluate(self, context: SymbolTable) -> int:
        a, b = self.children
        x, y = a.evaluate(context), b.evaluate(context)

        try:
            method = Binary_operation_node.OPERATIONS[self.value]
            
            return method(x, y)
        except KeyError:
            raise ValueError(f"{self.value} is not an Valid operation!")
