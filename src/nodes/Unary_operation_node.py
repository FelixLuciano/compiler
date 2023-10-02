import src.nodes as nodes
from src.SymbolTable import SymbolTable
from src.Token import Token


class Unary_operation_node(nodes.Node):
    value: Token.types

    OPERATIONS = {
        Token.types.OP_PLUS: lambda x: x,
        Token.types.OP_MINUS: lambda x: -x,
        Token.types.OP_NOT: lambda x: 0 if x == 1 else 1,
    }

    def evaluate(self, context: SymbolTable) -> int:
        x = self.children[0].evaluate(context)

        try:
            method = Unary_operation_node.OPERATIONS[self.value]
            
            return method(x)
        except KeyError:
            raise ValueError(f"{self.value} is not an Valid operation!")
