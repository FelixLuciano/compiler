from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class Identifier_reference_node(Abstract_node):
    def evaluate(self, context: SymbolTable) -> int:
        value = context.get(self.value)

        if isinstance(value, int):
            return value

        raise ValueError(f"{self.value} is not an valid reference!")
