import typing as T
from dataclasses import dataclass, field

from src.Typed_value import Typed_value


@dataclass
class SymbolTable:
    table: T.Dict[str, T.Tuple[Typed_value, int]] = field(default_factory=dict)

    RESERVED: T.Dict[str, Typed_value] = field(
        init=False,
        repr=False,
        default_factory=lambda: {
            "false": Typed_value(Typed_value.types.INT, 0),
            "true": Typed_value(Typed_value.types.INT, 1),
            "Println": Typed_value(Typed_value.types.FUNCTION, lambda *args: print(*(arg.value for arg in args))),
            "Scanln": Typed_value(Typed_value.types.FUNCTION, lambda: Typed_value(Typed_value.types.INT, int(input("")))),
        }
    )

    stack_pointer: int = 0

    def declare(self, identifier: str, type_: Typed_value.types) -> None:
        if identifier in self.RESERVED:
            raise KeyError(
                f"{identifier} couldn't be declared because it is a reserved keyword!"
            )
        elif identifier in self.table:
            raise KeyError(
                f"{identifier} couldn't be declared because it is was already declared!"
            )

        self.table[identifier] = (Typed_value(type_, None), SymbolTable.stack_pointer)

        SymbolTable.stack_pointer += 4

    def set(self, identifier: str, value: Typed_value) -> None:
        if identifier not in self.table:
            raise KeyError(f"{identifier} as not declared!")
    
        type_= self.table[identifier][0].type
        pointer = self.table[identifier][1]

        if (value.type != type_):
            raise KeyError(f"Couldn't assign {value.type.name} into an {type_.name} variable!")

        self.table[identifier] = (value, pointer)

    def get(self, identifier: str) -> T.Tuple[Typed_value, int]:
        if identifier in self.RESERVED:
            return (self.RESERVED[identifier], -1)
        elif identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"{identifier} was not assigned.")
