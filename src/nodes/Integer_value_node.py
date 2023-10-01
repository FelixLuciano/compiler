import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Integer_value_node(nodes.Node):
    value: int

    def evaluate(self, context: SymbolTable) -> int:
        return int(self.value)
