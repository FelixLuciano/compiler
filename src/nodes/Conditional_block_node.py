from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Conditional_block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable, program: Program):
        value: Typed_value = self.children[0].evaluate(context, program)
        else_label_name = f"LOOP_{self.id}"
        endif_label_name = f"ENDLOOP_{self.id}"

        if Typed_value.is_true(value):
            self.children[1].evaluate(context, program)
            program.write(f"JMP {endif_label_name}")
        elif (len(self.children) > 2):
            program.write(f"{else_label_name}:")
            self.children[2].evaluate(context, program)
        program.write(f"{endif_label_name}:")

        return Typed_value.NULL
