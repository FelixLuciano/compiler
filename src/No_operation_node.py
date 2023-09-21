from src.Abstract_node import Abstract_node

from src.SymbolTable import SymbolTable


class No_operation_node(Abstract_node):
    value : None

    def evaluate(self) -> None:
        return None
