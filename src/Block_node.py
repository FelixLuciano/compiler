from src.Abstract_node import Abstract_node


class Block_node(Abstract_node):
    def evaluate(self) -> None:
        for child in self.children:
            child.evaluate()
