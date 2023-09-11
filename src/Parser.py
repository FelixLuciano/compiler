from dataclasses import dataclass, field

from src.Token import Token
from src.Tokenizer import Tokenizer
from src.Abstract_node import Abstract_node
from src.Integer_value_node import Integer_value_node
from src.Unary_operation_node import Unary_operation_node
from src.Binary_operation_node import Binary_operation_node

@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    def parse_expression(self) -> Abstract_node:
        root = self.parse_term()

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
                root = Binary_operation_node(Token.types.PLUS, [root, next])
            elif operator == Token.types.MINUS:
                root = Binary_operation_node(Token.types.MINUS, [root, next])

        return root

    def parse_term(self) -> Abstract_node:
        root = self.parse_factor()

        while True:
            if self.tokenizer.next.check(Token.types.MULT):
                operator = Token.types.MULT
            elif self.tokenizer.next.check(Token.types.DIV):
                operator = Token.types.DIV
            else:
                break

            self.tokenizer.select_next()

            if operator == Token.types.MULT:
                root = Binary_operation_node(Token.types.MULT, [root, self.parse_factor()])
            elif operator == Token.types.DIV:
                root = Binary_operation_node(Token.types.DIV, [root, self.parse_factor()])

        return root
    
    def parse_factor(self):
        while self.tokenizer.next == Token.LAMBDA:
            self.tokenizer.select_next()

        if self.tokenizer.next.check(Token.types.DIGIT):
            value = self.tokenizer.next.value
            
            self.tokenizer.select_next()

            return Integer_value_node(value)
        elif self.tokenizer.next.check(Token.types.PLUS):
            self.tokenizer.select_next()
            return Unary_operation_node(Token.types.PLUS, [self.parse_factor()])
        elif self.tokenizer.next.check(Token.types.MINUS):
            self.tokenizer.select_next()
            return Unary_operation_node(Token.types.MINUS, [self.parse_factor()])
        elif self.tokenizer.next.check(Token.types.OPEN_PARENTHESIS):
            self.tokenizer.select_next()

            expression = self.parse_expression()

            if self.tokenizer.next.check(Token.types.CLOSE_PARENTHESIS):
                self.tokenizer.select_next()

                return expression
            else:
                raise ValueError(
                    f"Expected close parenthesis at {self.tokenizer.position}!"
                )
        else:
            raise ValueError(
                f"Unexpected token {self.tokenizer.next.type} at {self.tokenizer.position}!"
            )

    @staticmethod
    def run(code: str) -> Abstract_node:
        parser = Parser(Tokenizer(code))
        answer = parser.parse_expression()

        if parser.tokenizer.next != Token.EOF:
            print(answer, parser.tokenizer.next)
            raise ValueError(f'Invalid expression "{code}"')

        return answer
