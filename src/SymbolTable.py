import typing as T
from dataclasses import dataclass, field

from src.Typed_value import Typed_value


@dataclass
class SymbolTable:
    table: T.Dict[str, Typed_value] = field(default_factory=dict)
    parent: T.Optional["SymbolTable"] = field(default=None)

    RESERVED: T.Dict[str, Typed_value] = field(
        init=False,
        repr=False,
        default_factory=lambda: {
            "false": Typed_value(Typed_value.types.INT, 0),
            "true": Typed_value(Typed_value.types.INT, 1),
            "Println": Typed_value(Typed_value.types.NULL, lambda *args: print(*(arg.value for arg in args))),
            "Scanln": Typed_value(Typed_value.types.INT, lambda: Typed_value(Typed_value.types.INT, int(input("")))),
        }
    )

    def declare(self, identifier: str, type_: Typed_value.types) -> None:
        if identifier in self.RESERVED:
            raise KeyError(
                f"{identifier} couldn't be declared because it is a reserved keyword!"
            )
        elif identifier in self.table:
            raise KeyError(
                f"{identifier} couldn't be declared because it is was already declared!"
            )

        self.table[identifier] = Typed_value(type_, None)

    def set(self, identifier: str, value: Typed_value) -> None:
        if identifier not in self.table:
            raise KeyError(f"{identifier} as not declared!")
    
        type_ = self.table[identifier].type
        
        if (value.type != type_):
            raise KeyError(f"Couldn't assign {value.type.name} into an {type_.name} variable!")

        self.table[identifier] = value

    def get(self, identifier: str) -> Typed_value:
        if identifier in self.RESERVED:
            return self.RESERVED[identifier]
        elif identifier in self.table:
            return self.table[identifier]
        elif self.parent is not None:
            return self.parent.get(identifier)
        else:
            raise ValueError(f"{identifier} was not assigned.")
