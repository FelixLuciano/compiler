from src.Abstract_node import Abstract_node
from src.Token import Token


class Integer_value_node(Abstract_node):
    value : int

    def evaluate(self) -> int:
        return self.value
