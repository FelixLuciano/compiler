import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Iterator_block_node(nodes.Node):
    value: None

    def evaluate(self, context: SymbolTable) -> None:
        assignment, condition, step, block = self.children

        assignment.evaluate(context)
        while condition.evaluate(context) == True:
            block.evaluate(context)
            step.evaluate(context)
