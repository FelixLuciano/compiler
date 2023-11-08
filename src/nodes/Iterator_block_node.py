from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Iterator_block_node(nodes.Node):
    value: None = field(default=None)

    def evaluate(self, context: SymbolTable, program: Program):
        assignment, condition, step, block = self.children
        loop_label_name = f"LOOP_{self.i}"
        endloop_label_name = f"ENDLOOP_{self.i}"

        assignment.evaluate(context, program)
        program.write(loop_label_name + ":")
        while Typed_value.is_true(condition.evaluate(context, program)):
            block.evaluate(context, program)
            step.evaluate(context, program)
            program.disable()
        program.enable()
        program.write(
            f"JMP {loop_label_name}",
            f"{endloop_label_name}:",
        )

        return Typed_value.NULL
