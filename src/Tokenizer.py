import typing as T
from dataclasses import dataclass, field

from src.Token import Token, LAMBDA, END_OF_FILE


@dataclass
class Tokenizer:
    source: str = field()
    position: int = field(default=-1)
    next: Token = field(init=False, default_factory=lambda: LAMBDA)

    def get(self, index):
        try:
            return self.source[index]
        except IndexError:
            return "\n"

    def select_next(self):
        index = self.position
        state = Token.types.LAMBDA
        stack = []

        if index >= len(self.source):
            self.next = END_OF_FILE
            return

        for index in range(self.position, len(self.source) + 1):
            next = self.get(index)
            next_state = Token.types.get(next)

            if next_state is None:
                raise ValueError(f"Invalid token {next} at {self.position}!")
            elif state == Token.types.LAMBDA:    
                if next_state == Token.types.SPACE:
                    continue

                state = next_state

            if next_state == Token.types.NUMBER and state == Token.types.IDENTIFIER:
                next_state = state

            if state in Token.CHAINING_TOKENS:
                if state != next_state:
                    break
            else:
                if len(stack) > 0:
                    break

            stack.append(next)

        self.position = index
        self.next = Token(state, "".join(stack))

    def assert_type(self, type: Token.types):
        if not self.next.check(type):
            raise ValueError(
                f"Expected token {type.name} and got {self.next.type.name} at {self.position}!"
            )
