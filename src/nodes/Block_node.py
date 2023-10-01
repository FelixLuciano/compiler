import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Block_node(nodes.Node):
    def evaluate(self, context: SymbolTable) -> None:
        for child in self.children:
            child.evaluate(context)
