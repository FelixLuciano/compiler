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
        CHAINED_SYMBOL = auto()
        ASSIGNMENT = auto()
        ASSIGNMENT_PLUS = auto()
        ASSIGNMENT_MINUS = auto()
        ASSIGNMENT_MULT = auto()
        ASSIGNMENT_DIV = auto()
        OP_PLUS = auto()
        OP_MINUS = auto()
        OP_MULT = auto()
        OP_DIV = auto()
        OP_AND = auto()
        OP_OR = auto()
        OP_NOT = auto()
        OP_EQUAL = auto()
        OP_NOT_EQUAL = auto()
        OP_GREATER = auto()
        OP_LOWER = auto()
        OP_GREATER_EQUAL = auto()
        OP_LOWER_EQUAL = auto()
        OPEN_PARENTHESIS = auto()
        CLOSE_PARENTHESIS = auto()
        OPEN_BRACES = auto()
        CLOSE_BRACES = auto()
        SEPARATOR = auto()
        HARD_SEPARATOR = auto()
        IF_STATEMENT = auto()
        ELSE_STATEMENT = auto()
        FOR_STATEMENT = auto()

        @classmethod
        def get(cls, value: str, is_eval: bool = False):
            try:
                if len(value) == 0:
                    return cls.LAMBDA
                elif len(value) == 1:
                    if value == "\n":
                        return cls.END_OF_LINE
                    if value in string.whitespace:
                        return cls.SPACE
                    elif value in string.digits:
                        return cls.NUMBER
                    elif value in string.ascii_letters + "_":
                        return cls.IDENTIFIER
                    elif value in "!&-+=|<>" and not is_eval:
                        return cls.CHAINED_SYMBOL

                return {
                    "=": cls.ASSIGNMENT,
                    "+=": cls.ASSIGNMENT_PLUS,
                    "-=": cls.ASSIGNMENT_MINUS,
                    "*=": cls.ASSIGNMENT_MULT,
                    "/=": cls.ASSIGNMENT_DIV,
                    "+": cls.OP_PLUS,
                    "-": cls.OP_MINUS,
                    "*": cls.OP_MULT,
                    "/": cls.OP_DIV,
                    "(": cls.OPEN_PARENTHESIS,
                    ")": cls.CLOSE_PARENTHESIS,
                    "{": cls.OPEN_BRACES,
                    "}": cls.CLOSE_BRACES,
                    ",": cls.SEPARATOR,
                    ";": cls.HARD_SEPARATOR,
                    "&&": cls.OP_AND,
                    "||": cls.OP_OR,
                    "!": cls.OP_NOT,
                    "==": cls.OP_EQUAL,
                    "!=": cls.OP_NOT_EQUAL,
                    ">": cls.OP_GREATER,
                    "<": cls.OP_LOWER,
                    ">=": cls.OP_GREATER_EQUAL,
                    "<=": cls.OP_LOWER_EQUAL,
                    "if": cls.IF_STATEMENT,
                    "else": cls.ELSE_STATEMENT,
                    "for": cls.FOR_STATEMENT,
                }[value]
            except KeyError:
                return None

    def check(self, type: types):
        return self.type == type


LAMBDA = Token(Token.types.LAMBDA, "")
END_OF_FILE = Token(Token.types.END_OF_FILE, "")
Token.CHAINING_TOKENS = set(
    (Token.types.SPACE, Token.types.NUMBER, Token.types.IDENTIFIER, Token.types.CHAINED_SYMBOL)
)
