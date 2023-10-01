import src.nodes as nodes
from src.SymbolTable import SymbolTable


class Identifier_assignment_node(nodes.Node):
    value: str

    def evaluate(self, context: SymbolTable) -> int:
        value = self.children[0].evaluate(context)

        context.set(self.value, value)

        return value
