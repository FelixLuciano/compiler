import string
import typing as T
from enum import Enum, auto
from dataclasses import dataclass, field


@dataclass
class Token:
    type: "types" = field()
    value: str = field()

    CHAINING_TOKENS: T.Set["types"] = field(init=False, repr=False)

    class types(Enum):
        LAMBDA = auto()
        SPACE = auto()
        END_OF_LINE = auto()
        END_OF_FILE = auto()
        NUMBER = auto()
        IDENTIFIER = auto()
        ASSIGNMENT = auto()
        OP_PLUS = auto()
        OP_MINUS = auto()
        OP_MULT = auto()
        OP_DIV = auto()
        OPEN_PARENTHESIS = auto()
        CLOSE_PARENTHESIS = auto()
        SEPARATOR = auto()

        @classmethod
        def get(cls, value: str):
            if len(value) == 0:
                return cls.LAMBDA
            elif value == "\n":
                return cls.END_OF_LINE
            if value in string.whitespace:
                return cls.SPACE
            if value in string.digits:
                return cls.NUMBER
            if value in string.ascii_letters + "_":
                return cls.IDENTIFIER
            if value == "=":
                return cls.ASSIGNMENT
            elif value == "+":
                return cls.OP_PLUS
            elif value == "-":
                return cls.OP_MINUS
            elif value == "*":
                return cls.OP_MULT
            elif value == "/":
                return cls.OP_DIV
            elif value == "(":
                return cls.OPEN_PARENTHESIS
            elif value == ")":
                return cls.CLOSE_PARENTHESIS
            elif value == ",":
                return cls.SEPARATOR
            else:
                return None

    def check(self, type: types):
        return self.type == type


LAMBDA = Token(Token.types.LAMBDA, "")
END_OF_FILE = Token(Token.types.END_OF_FILE, "")
Token.CHAINING_TOKENS = set((Token.types.SPACE, Token.types.NUMBER, Token.types.IDENTIFIER))
