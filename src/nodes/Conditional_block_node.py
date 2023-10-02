import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Conditional_block_node(nodes.Node):
    value: None

    def evaluate(self, context: SymbolTable) -> None:
        value = self.children[0].evaluate(context)

        if (value == 1):
            self.children[1].evaluate(context)
        elif (len(self.children) > 2):
            self.children[2].evaluate(context)
