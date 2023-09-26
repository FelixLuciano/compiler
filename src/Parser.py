from dataclasses import dataclass, field

from src.Token import Token
from src.Pre_processing import Pre_processing
from src.Tokenizer import Tokenizer
from src.Abstract_node import Abstract_node
from src.Block_node import Block_node
from src.No_operation_node import No_operation_node
from src.Integer_value_node import Integer_value_node
from src.Unary_operation_node import Unary_operation_node
from src.Binary_operation_node import Binary_operation_node
from src.Identifier_assignment_node import Identifier_assignment_node
from src.Identifier_reference_node import Identifier_reference_node
from src.Identifier_call_node import Identifier_call_node


@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    @staticmethod
    def run(code: str) -> Abstract_node:
        tokenizer = Tokenizer(Pre_processing.filter(code))

        tokenizer.select_next()

        parser = Parser(tokenizer)
        answer = parser.parse_block()

        if not tokenizer.next.check(Token.types.END_OF_FILE):
            raise ValueError(f'Invalid expression "{code}"')

        return answer

    def parse_block(self) -> Block_node:
        statements = []

        while not self.check(Token.types.END_OF_FILE):
            statement = self.parse_statement()

            statements.append(statement)

        return Block_node(None, statements)

    def parse_statement(self, endl=True):
        statement = No_operation_node()

        if self.check(Token.types.IDENTIFIER):
            identifier = self.get_then_consume()

            if self.check_then_consume(Token.types.ASSIGNMENT):
                statement = Identifier_assignment_node(
                    value=identifier.value,
                    children=[
                        self.parse_statement(False),
                    ],
                )
            elif self.check_then_consume(Token.types.OPEN_PARENTHESIS):
                arguments = []

                while not self.check_then_consume(Token.types.CLOSE_PARENTHESIS):
                    arguments.append(self.parse_expression())

                    if self.check_then_consume(Token.types.SEPARATOR):
                        continue
                    elif self.check(Token.types.END_OF_LINE):
                        raise ValueError(
                            f"Expected , or ) after expression at {self.tokenizer.position}!"
                        )

                statement = Identifier_call_node(
                    value=identifier.value,
                    children=arguments,
                )
        elif not self.check(Token.types.END_OF_LINE):
            return self.parse_expression()

        if endl:
            if not self.check(Token.types.END_OF_FILE):
                self.expect_then_consume(Token.types.END_OF_LINE)

        return statement

    def parse_expression(self) -> Abstract_node:
        root = self.parse_term()

        while self.check_any(Token.types.OP_PLUS, Token.types.OP_MINUS):
            root = Binary_operation_node(
                value=self.get_then_consume().type,
                children=[
                    root,
                    self.parse_term(),
                ],
            )

        return root

    def parse_term(self) -> Abstract_node:
        root = self.parse_factor()

        while self.check_any(Token.types.OP_MULT, Token.types.OP_DIV):
            root = Binary_operation_node(
                value=self.get_then_consume().type,
                children=[
                    root,
                    self.parse_factor(),
                ],
            )

        return root

    def parse_factor(self) -> Abstract_node:
        if self.check(Token.types.NUMBER):
            return Integer_value_node(value=self.get_then_consume().value)
        if self.check(Token.types.IDENTIFIER):
            return Identifier_reference_node(value=self.get_then_consume().value)
        elif self.check_then_consume(Token.types.OP_PLUS):
            return Unary_operation_node(
                value=Token.types.OP_PLUS, children=[self.parse_factor()]
            )
        elif self.check_then_consume(Token.types.OP_MINUS):
            return Unary_operation_node(
                value=Token.types.OP_MINUS, children=[self.parse_factor()]
            )
        elif self.check_then_consume(Token.types.OPEN_PARENTHESIS):
            expression = self.parse_expression()

            self.expect_then_consume(Token.types.CLOSE_PARENTHESIS)

            return expression

        raise ValueError(
            f"Unexpected token {self.tokenizer.next.type.name} at {self.tokenizer.position}!"
        )

    def consume(self):
        self.tokenizer.select_next()

    def get_then_consume(self):
        next = self.tokenizer.next

        self.consume()

        return next

    def check(self, type_: Token.types):
        return self.tokenizer.next.check(type_)

    def check_any(self, *types: Token.types):
        return any(self.check(type_) for type_ in types)

    def check_then_consume(self, type_: Token.types):
        if self.check(type_):
            self.consume()

            return True

        return False

    def expect_then_consume(self, type_: Token.types):
        if self.check_then_consume(type_):
            return

        raise ValueError(
            f"Expected {type_.name} at {self.tokenizer.position}, instead got {self.tokenizer.next.type.name}!"
        )
