import src.nodes as nodes
from src.SymbolTable import SymbolTable
from src.Token import Token


class Unary_operation_node(nodes.Node):
    value: Token.types

    def evaluate(self, context: SymbolTable) -> int:
        if self.value == Token.types.OP_PLUS:
            return self.children[0].evaluate(context)
        elif self.value == Token.types.OP_MINUS:
            return self.children[0].evaluate(context) * -1

        raise ValueError(f"{self.value} is not an Valid operation!")
