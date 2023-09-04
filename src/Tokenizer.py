import typing as T
from dataclasses import dataclass, field

from src.Token import Token


@dataclass
class Tokenizer:
    source: str = field()
    position: int = field(default=-1)
    next: Token = field(init=False, default_factory=lambda: Token.LAMBDA)

    @property
    def current(self):
        return self.get(self.position)

    def get(self, index):
        try:
            return self.source[index]
        except IndexError:
            return "\0"

    def select_next(self):
        type_ = Token.types.LAMBDA
        value = 0

        while True:
            next = self.get(self.position + 1)
            peek = Token.types.get(next)

            if peek == Token.types.SPACE:
                pass
            elif type_ == Token.types.LAMBDA:
                type_ = peek
            elif peek is None:
                raise ValueError(f"Invalid token {next} at {self.position}!")
            elif type_ != peek and peek != Token.types.SPACE:
                break

            if peek == Token.types.EOF:
                self.position = len(self.source)
                self.next = Token.EOF
                return
            elif peek == Token.types.SPACE:
                pass
            elif peek == Token.types.DIGIT:
                value = int(next) + value * 10
            elif peek in (
                Token.types.PLUS,
                Token.types.MINUS,
                Token.types.MULT,
                Token.types.DIV,
            ):
                pass
            else:
                raise ValueError(
                    f'Unexpected token {peek.name} "{next}" at {self.position}!'
                )

            self.position += 1

            if peek not in Token.types.CHAINING_TYPES:
                break

        self.next = Token(type_.name, value)

    def assert_type(self, type: Token.types):
        if not self.next.check(type):
            raise ValueError(
                f"Expected token {type.name} and got {self.next.type} at {self.position}!"
            )
