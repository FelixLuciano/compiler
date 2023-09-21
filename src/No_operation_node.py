from src.Abstract_node import Abstract_node


class No_operation_node(Abstract_node):
    value : None

    def evaluate(self) -> None:
        return None
