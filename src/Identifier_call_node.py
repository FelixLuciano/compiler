from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class Identifier_call_node(Abstract_node):
    def evaluate(self, context: SymbolTable) -> None:
        func = context.get(self.value)
        args = (child.evaluate(context) for child in self.children)

        if callable(func):
            return func(*args)
        else:
            raise ValueError(f"{self.value} is not callable!")
