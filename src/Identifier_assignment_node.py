from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class Identifier_assignment_node(Abstract_node):
    value: str

    def evaluate(self, context: SymbolTable) -> int:
        value = self.children[0].evaluate(context)

        context.set(self.value, value)

        return value
