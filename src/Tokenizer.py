import typing as T
import string
from dataclasses import dataclass, field

from src.Token import Token


@dataclass
class Tokenizer:
    source: str = field()
    position: int = field(init=False, default=0)
    next: Token = field(init=False, repr=False, default=None)

    def select_next(self, expect: T.Optional[Token.types] = None):
        if expect is not None and self.next.type != expect:
            raise ValueError(f"Expected {expect} and got {self.next.type} {self.source[self.position]} at {self.position}")

        self._skip_whitespaces()

        peek = self._peek_type()
        value = 0

        if peek == Token.types.NUMBER:
            _digit_count = self._count_characters_from_position(string.digits)
            print(self.position, _digit_count, self.source[self.position:self.position+_digit_count])
            value = int(self.source[self.position:self.position+_digit_count])
            self.position += _digit_count
        elif peek in (
            Token.types.PLUS,
            Token.types.MINUS,
            Token.types.MULT,
            Token.types.DIV,
        ):
            self.position += 1

        token = self.next
        self.next = Token(peek.name, value)

        return token

    def _skip_whitespaces(self):
        self.position += self._count_characters_from_position(string.whitespace)

    def _count_characters_from_position(self, dictionary: T.LiteralString):
        for position in range(self.position, len(self.source)):
            if self.source[position] not in dictionary:
                break

        return position - self.position

    def _peek_type(self):
        try:
            return Token.types.get(self.source[self.position])
        except IndexError:
            return Token.types.EOS

    def __post_init__(self):
        self.select_next()
