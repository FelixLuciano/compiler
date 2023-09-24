from src.Abstract_node import Abstract_node
from src.Token import Token

from src.SymbolTable import SymbolTable


class Unary_operation_node(Abstract_node):
    value: Token.types

    def evaluate(self, context: SymbolTable) -> int:
        if self.value == Token.types.OP_PLUS:
            return self.children[0].evaluate(context)
        elif self.value == Token.types.OP_MINUS:
            return self.children[0].evaluate(context) * -1

        raise ValueError(f"{self.value} is not an Valid operation!")
