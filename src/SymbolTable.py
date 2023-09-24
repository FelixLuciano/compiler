import typing as T
from dataclasses import dataclass, field


@dataclass
class SymbolTable:
    table : T.Dict[str, int | T.Callable] = field(default_factory=dict)

    RESERVED = {
        "Println": print
    }

    def set(self, identifier: str, value: int) -> None:
        self.table[identifier] = value
    
    def get(self, identifier: str) -> T.Union[int, T.Callable]:
        if identifier in self.RESERVED:
            return self.RESERVED[identifier]
        elif identifier in self.table:
            return self.table[identifier]
        else:
            raise ValueError(f"{identifier} was not assigned.")
