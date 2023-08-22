import string
from enum import Enum, auto
from dataclasses import dataclass, field


@dataclass
class Token:
    type: str = field()
    value: int = field()

    class types(Enum):
        LAMBDA = None
        EOS = auto()
        NUMBER = auto()
        PLUS = auto()
        MINUS = auto()

        @classmethod
        def get(cls, value: str):
            if value in string.digits:
                return cls.NUMBER
            elif value == "+":
                return cls.PLUS
            elif value == "-":
                return cls.MINUS
            
            raise AttributeError(f"\"{value}\" is not valid!")
