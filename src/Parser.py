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
        answer = self.parse_factor()

        while True:
            if self.tokenizer.next.check(Token.types.MULT):
                operator = Token.types.MULT
            elif self.tokenizer.next.check(Token.types.DIV):
                operator = Token.types.DIV
            else:
                break

            self.tokenizer.select_next()

            if operator == Token.types.MULT:
                answer *= self.parse_factor()
            elif operator == Token.types.DIV:
                answer //= self.parse_factor()

        return answer
    
    def parse_factor(self):
        while self.tokenizer.next == Token.LAMBDA:
            self.tokenizer.select_next()

        if self.tokenizer.next.check(Token.types.DIGIT):
            answer = self.tokenizer.next.value
            
            self.tokenizer.select_next()

            return answer
        elif self.tokenizer.next.check(Token.types.PLUS):
            self.tokenizer.select_next()
            return self.parse_factor()
        elif self.tokenizer.next.check(Token.types.MINUS):
            self.tokenizer.select_next()
            return self.parse_factor() * -1
        elif self.tokenizer.next.check(Token.types.OPEN_PARENTHESIS):
            self.tokenizer.select_next()

            answer = self.parse_expression()

            if self.tokenizer.next.check(Token.types.CLOSE_PARENTHESIS):
                self.tokenizer.select_next()

                return answer
            else:
                raise ValueError(
                    f"Expected close parenthesis at {self.tokenizer.position}!"
                )
        else:
            raise ValueError(
                f"Unexpected token {self.tokenizer.next.type} at {self.tokenizer.position}!"
            )

    @staticmethod
    def run(code: str) -> int:
        parser = Parser(Tokenizer(code))
        answer = parser.parse_expression()

        if parser.tokenizer.next != Token.EOF:
            print(answer, parser.tokenizer.next)
            raise ValueError(f'Invalid expression "{code}"')

        return answer
