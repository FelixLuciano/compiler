import typing as T
from dataclasses import dataclass, field


@dataclass
class SymbolTable:
    table: T.Dict[str, T.Any] = field(default_factory=dict)

    RESERVED = {
        "Println": print,
        "Scanln": lambda: int(input("")),
    }

    def set(self, identifier: str, value: int) -> None:
        if identifier not in self.RESERVED:
            self.table[identifier] = value
        else:
            raise KeyError(
                f"{identifier} couldn't be assigned because it is a reserved keyword!"
            )

    def get(self, identifier: str) -> T.Union[int, T.Callable]:
        if identifier in self.RESERVED:
            return self.RESERVED[identifier]
        elif identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"{identifier} was not assigned.")
