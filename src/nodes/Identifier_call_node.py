import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Identifier_call_node(nodes.Node):
    def evaluate(self, context: SymbolTable) -> None:
        func = context.get(self.value)
        args = (child.evaluate(context) for child in self.children)

        if callable(func):
            return func(*args)
        else:
            raise ValueError(f"{self.value} is not callable!")
