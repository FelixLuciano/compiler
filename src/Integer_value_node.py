from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class Integer_value_node(Abstract_node):
    value: int

    def evaluate(self, context: SymbolTable) -> int:
        return int(self.value)
