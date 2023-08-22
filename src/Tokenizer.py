import typing as T
import string
from dataclasses import dataclass, field

from src.Token import Token


@dataclass
class Tokenizer:
    source: str = field()
    position: int = field(init=False, default=0)
    next: Token = field(init=False, repr=False, default=None)

    def selectNext(self):
        self._skip_whitespaces()

        peek = self._peek_type()

        if peek == Token.types.NUMBER:
            value = self._tokenize_number()
        elif peek == Token.types.PLUS:
            value = 1
            self.position += 1
        elif peek == Token.types.MINUS:
            value = -1
            self.position += 1
        else:
            value = peek.value

        token = self.next
        self.next = Token(peek.name, value)

        return token

    def _skip_whitespaces(self):
        self.position += self._count_characters_from_position(string.whitespace)

    def _count_characters_from_position(self, dictionary: T.LiteralString):
        count = 0

        while self.position + count < len(self.source) and self.source[self.position + count] in dictionary:
            count += 1

        return count

    def _peek_type(self):
        try:
            return Token.types.get(self.source[self.position])
        except IndexError:
            return Token.types.EOS

    def _tokenize_number(self):
        digit_count = self._count_characters_from_position(string.digits)
        value_input = self.source[self.position:self.position+digit_count]
        self.position += digit_count

        return int(value_input)

    def __post_init__(self):
        self.selectNext()
