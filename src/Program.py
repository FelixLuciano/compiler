import os
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Program:
    path: Path = field()
    can_write: bool = field(default=True, init=False, repr=False)
    ident_width: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.clear()

    def clear(self):
        if self.path.exists():
            os.remove(self.path)

    def enable(self):
        self.can_write = True

    def disable(self):
        self.can_write = False

    def indent(self):
        self.ident_width += 4

    def unindent(self):
        self.ident_width -= 4

    def write(self, *text: str) -> None:
        if self.can_write:
            with open(self.path, "at", encoding="utf-8") as f:
                f.writelines((" "* self.ident_width + line + "\n" for line in text))

    def build_header(self):
        self.write(
            "; constantes",
            "SYS_EXIT equ 1",
            "SYS_READ equ 3",
            "SYS_WRITE equ 4",
            "STDIN equ 0",
            "STDOUT equ 1",
            "True equ 1",
            "False equ 0",
            "",
            "segment .data",
            "",
            'formatin: db "%d", 0',
            'formatout: db "%d", 10, 0 ; newline, nul terminator',
            "scanint: times 4 db 0 ; 32-bits integer = 4 bytes",
            "",
            "segment .bss  ; variaveis",
            "extern fflush",
            "extern stdout",
            "res RESB 1",
            "",
            "section .text",
            "global main ; linux",
            ";global _main ; windows",
            "extern scanf ; linux",
            "extern printf ; linux",
            ";extern _scanf ; windows",
            ";extern _printf; windows",
            "extern fflush ; linux",
            ";extern _fflush ; windows",
            "extern stdout ; linux",
            ";extern _stdout ; windows",
            "",
            "; subrotinas if/while",
            "binop_je:",
            "JE binop_true",
            "JMP binop_false",
            "",
            "binop_jg:",
            "JG binop_true",
            "JMP binop_false",
            "",
            "binop_jl:",
            "JL binop_true",
            "JMP binop_false",
            "",
            "binop_false:",
            "MOV EAX, False  ",
            "JMP binop_exit",
            "binop_true:",
            "MOV EAX, True",
            "binop_exit:",
            "RET",
            "",
            "main:",
            "",
            "PUSH EBP ; guarda o base pointer",
            "MOV EBP, ESP ; estabelece um novo base pointer",
            "",
            "; codigo gerado pelo compilador abaixo",
        )

    def build_footer(self):
        self.write(
            "",
            "; interrupcao de saida (default)",
            "PUSH DWORD [stdout]",
            "CALL fflush",
            "ADD ESP, 4",
            "MOV ESP, EBP",
            "POP EBP",
            "MOV EAX, 1",
            "XOR EBX, EBX",
            "INT 0x80",
        )
