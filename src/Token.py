import string
from enum import Enum, auto
from dataclasses import dataclass, field


@dataclass
class Token:
    type: str = field()
    value: int = field()

    class types(Enum):
        LAMBDA = None
        EOF = auto()
        NUMBER = auto()
        PLUS = auto()
        MINUS = auto()
        MULT = auto()
        DIV = auto()

        @classmethod
        def get(cls, value: str):
            if value in string.digits:
                return cls.NUMBER
            elif value == "+":
                return cls.PLUS
            elif value == "-":
                return cls.MINUS
            elif value == "*":
                return cls.MULT
            elif value == "/":
                return cls.DIV
            
            raise ValueError(f"\"{value}\" is not a valid token!")
