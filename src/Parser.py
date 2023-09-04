from dataclasses import dataclass, field

from src.Token import Token
from src.Tokenizer import Tokenizer


@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    def parse_expression(self) -> int:
        answer = self.parse_term()

        while True:
            if self.tokenizer.next.check(Token.types.PLUS):
                operator = Token.types.PLUS
            elif self.tokenizer.next.check(Token.types.MINUS):
                operator = Token.types.MINUS
            else:
                break

            self.tokenizer.select_next()

            next = self.parse_term()

            if operator == Token.types.PLUS:
                answer += next
            elif operator == Token.types.MINUS:
                answer -= next

        return answer

    def parse_term(self) -> int:
        answer = 0

        while self.tokenizer.next == Token.LAMBDA:
            self.tokenizer.select_next()

        if self.tokenizer.next.check(Token.types.DIGIT):
            answer = self.tokenizer.next.value
        else:
            raise ValueError(
                f"Unexpected token {self.tokenizer.next.type} at {self.tokenizer.position}!"
            )

        self.tokenizer.select_next()

        while True:
            if self.tokenizer.next.check(Token.types.MULT):
                operator = Token.types.MULT
            elif self.tokenizer.next.check(Token.types.DIV):
                operator = Token.types.DIV
            else:
                break

            self.tokenizer.select_next()

            if self.tokenizer.next.check(Token.types.DIGIT):
                if operator == Token.types.MULT:
                    answer *= self.tokenizer.next.value
                elif operator == Token.types.DIV:
                    answer //= self.tokenizer.next.value
            else:
                raise ValueError(
                    f"Unexpected token {self.tokenizer.next.type} at {self.tokenizer.position}!"
                )

            self.tokenizer.select_next()

        return answer

    @staticmethod
    def run(code: str) -> int:
        parser = Parser(Tokenizer(code))
        answer = parser.parse_expression()

        if parser.tokenizer.next != Token.EOF:
            print(answer, parser.tokenizer.next)
            raise ValueError(f'Invalid expression "{code}"')

        return answer
