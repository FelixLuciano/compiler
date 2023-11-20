from dataclasses import dataclass, field

import src.nodes as nodes
from src.SymbolTable import SymbolTable, Typed_value
from src.Program import Program


@dataclass
class Identifier_call_node(nodes.Node):
    value: str = field()

    def evaluate(self, context: SymbolTable, program: Program):
        func, pointer = context.get(self.value)
        args = [child.evaluate(context, program) for child in self.children]

        if self.value == "Scanln":
            program.write(
                "PUSH scanint ; Endereço de memória de suporte",
                "PUSH formatin ; Formato de entrada (int)",
                "CALL scanf",
                "ADD ESP, 8 ; Remove os argumentos da pilha",
                "MOV EAX, DWORD [scanint] ; Retorna o valor lido em EAX",
            )
        elif self.value == "Println":
            program.write(
                "PUSH EAX",
                "PUSH formatout ; Formato int de saída",
                "CALL printf",
                "ADD ESP, 8 ; Remove os argumentos da pilha",
            )

        if isinstance(func.value, nodes.Function):
            child_context = func.value.before_evaluate(context, *args)

            value =  func.value.evaluate(child_context)

            if value.type != func.type:
                raise TypeError(f"Function of type {func.type.name} cannot return type {value.type.name}!")

            return value
        elif callable(func.value):
            return func.value(*args)

        raise ValueError(f"{self.value} is not a function!")
