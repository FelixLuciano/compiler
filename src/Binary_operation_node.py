from src.Abstract_node import Abstract_node
from src.Token import Token


class Binary_operation_node(Abstract_node):
    value : Token.types

    def evaluate(self) -> int:
        if self.value == Token.types.OP_PLUS:
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == Token.types.OP_MINUS:
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == Token.types.OP_MULT:
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == Token.types.OP_DIV:
            return self.children[0].evaluate() // self.children[1].evaluate()
    
        raise ValueError(f"{self.value} is not an Valid operation!")
