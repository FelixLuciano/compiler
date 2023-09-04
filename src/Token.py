import string
import typing as T
from enum import Enum, auto
from dataclasses import dataclass, field


@dataclass
class Token:
    type: str = field()
    value: int = field()

    LAMBDA: "Token" = field(init=False, repr=False)
    EOF: "Token" = field(init=False, repr=False)

    class types(Enum):
        LAMBDA = auto()
        SPACE = auto()
        DIGIT = auto()
        PLUS = auto()
        MINUS = auto()
        MULT = auto()
        DIV = auto()
        EOF = auto()

        CHAINING_TYPES: T.Tuple["Token.types"]

        @classmethod
        def get(cls, value: str):
            if len(value) == 0:
                return cls.LAMBDA
            if value in string.whitespace:
                return cls.SPACE
            if value in string.digits:
                return cls.DIGIT
            elif value == "+":
                return cls.PLUS
            elif value == "-":
                return cls.MINUS
            elif value == "*":
                return cls.MULT
            elif value == "/":
                return cls.DIV
            elif value == "\0":
                return cls.EOF
            else:
                return None

    def check(self, type: types):
        return self.type == type.name


Token.LAMBDA = Token(Token.types.LAMBDA.name, None)
Token.EOF = Token(Token.types.EOF.name, None)
Token.types.CHAINING_TYPES = (Token.types.SPACE, Token.types.DIGIT)

Token.types.CHAINING_TYPES
