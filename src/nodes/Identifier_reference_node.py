import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Identifier_reference_node(nodes.Node):
    def evaluate(self, context: SymbolTable) -> int:
        value = context.get(self.value)

        if isinstance(value, int):
            return value

        raise ValueError(f"{self.value} is not an valid reference!")
