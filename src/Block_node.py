from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class Block_node(Abstract_node):
    def evaluate(self, context: SymbolTable) -> None:
        for child in self.children:
            child.evaluate(context)
