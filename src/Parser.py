from dataclasses import dataclass, field

import src.nodes as nodes
from src.Pre_processing import Pre_processing
from src.Token import Token
from src.Tokenizer import Tokenizer


@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    @staticmethod
    def run(code: str) -> nodes.Node:
        tokenizer = Tokenizer(Pre_processing.filter(code))

        tokenizer.select_next()

        parser = Parser(tokenizer)
        answer = parser.parse_file()

        if not tokenizer.next.check(Token.types.END_OF_FILE):
            raise ValueError(f'Invalid expression "{code}"')

        return answer

    def parse_file(self) -> nodes.Block:
        statements = []

        while not self.check(Token.types.END_OF_FILE):
            statement = self.parse_statement()

            statements.append(statement)

        return nodes.Block(None, statements)

    def parse_block(self) -> nodes.Block:
        statements = []

        self.expect_then_consume(Token.types.OPEN_BRACES)

        while not self.check_then_consume(Token.types.CLOSE_BRACES):
            statement = self.parse_statement()

            statements.append(statement)

        return nodes.Block(None, statements)

    def parse_statement(self, endl=True):
        statement = nodes.No_operation()

        if self.check(Token.types.IDENTIFIER):
            statement = self.parse_assignment()
        elif self.check_then_consume(Token.types.IF_STATEMENT):
            children = [self.parse_boolean_expression(), self.parse_block()]

            while self.check_then_consume(Token.types.END_OF_LINE):
                continue

            if self.check_then_consume(Token.types.ELSE_STATEMENT):
                children.append(self.parse_block())

            return nodes.Conditional_block(
                value=None,
                children=children,
            )
        elif self.check_then_consume(Token.types.FOR_STATEMENT):
            assignment = self.parse_assignment()
            self.expect_then_consume(Token.types.HARD_SEPARATOR)
            condition = self.parse_boolean_expression()
            self.expect_then_consume(Token.types.HARD_SEPARATOR)
            step = self.parse_assignment()
            block = self.parse_block()

            return nodes.Iterator_block(
                value=None,
                children=[
                    assignment,
                    condition,
                    step,
                    block,
                ],
            )
        elif not self.check(Token.types.END_OF_LINE):
            return self.parse_boolean_expression()

        if endl:
            if not self.check(Token.types.END_OF_FILE):
                self.expect_then_consume(Token.types.END_OF_LINE)

        return statement
    
    def parse_assignment(self, root=True):
        if self.check(Token.types.IDENTIFIER):
            expression = self.parse_boolean_expression()

            if isinstance(expression, nodes.Identifier_reference):
                operation = None

                if self.check_then_consume(Token.types.ASSIGNMENT_PLUS):
                    operation = Token.types.OP_PLUS
                elif self.check_then_consume(Token.types.ASSIGNMENT_MINUS):
                    operation = Token.types.OP_MINUS
                elif self.check_then_consume(Token.types.ASSIGNMENT_MULT):
                    operation = Token.types.OP_MULT
                elif self.check_then_consume(Token.types.ASSIGNMENT_DIV):
                    operation = Token.types.OP_DIV

                if operation is not None:
                    return nodes.Identifier_assignment(
                        value=expression.value,
                        children=[
                            nodes.Binary_operation(
                                value=operation,
                                children=[
                                    expression,
                                    self.parse_assignment(False),
                                ]
                            ),
                        ],
                    )

                if self.check_then_consume(Token.types.ASSIGNMENT):
                    return nodes.Identifier_assignment(
                        value=expression.value,
                        children=[
                            self.parse_assignment(False),
                        ],
                    )

            return expression
        elif not root:
            return self.parse_boolean_expression()

        self.raise_unexpected_token()

    def parse_call(self, reference: nodes.Identifier_reference) -> nodes.Identifier_call:
        self.expect_then_consume(Token.types.OPEN_PARENTHESIS)

        arguments = []
        while not self.check_then_consume(Token.types.CLOSE_PARENTHESIS):
            arguments.append(self.parse_boolean_expression())

            if self.check_then_consume(Token.types.SEPARATOR):
                continue
            elif self.check(Token.types.END_OF_LINE):
                self.raise_unexpected_token()

        return nodes.Identifier_call(
            value=reference.value,
            children=arguments,
        )
    
    def parse_boolean_expression(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_boolean_term, Token.types.OP_EQUAL, Token.types.OP_NOT_EQUAL, Token.types.OP_GREATER, Token.types.OP_LOWER, Token.types.OP_GREATER_EQUAL, Token.types.OP_LOWER_EQUAL)

    def parse_boolean_term(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_boolean_factor, Token.types.OP_OR)
    
    def parse_boolean_factor(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_expression, Token.types.OP_AND)

    def parse_expression(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_term, Token.types.OP_PLUS, Token.types.OP_MINUS)

    def parse_term(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_factor, Token.types.OP_MULT, Token.types.OP_DIV)

    def parse_binary_operation(self, get_factor, *operators):
        root = get_factor()

        while self.check_any(*operators):
            root = nodes.Binary_operation(
                value=self.get_then_consume().type,
                children=[
                    root,
                    get_factor(),
                ],
            )

        return root

    def parse_factor(self) -> nodes.Node:
        if self.check(Token.types.NUMBER):
            return nodes.Integer_value(value=self.get_then_consume().value)
        elif self.check_any(Token.types.OP_PLUS, Token.types.OP_MINUS, Token.types.OP_NOT):
            return nodes.Unary_operation(
                value=self.get_then_consume().type,
                children=[self.parse_factor()]
            )
        elif self.check_then_consume(Token.types.OPEN_PARENTHESIS):
            expression = self.parse_boolean_expression()

            self.expect_then_consume(Token.types.CLOSE_PARENTHESIS)

            return expression
        elif self.check(Token.types.IDENTIFIER):
            identifier = self.get_then_consume()

            if self.check(Token.types.OPEN_PARENTHESIS):
                return self.parse_call(nodes.Identifier_reference(identifier.value))

            return nodes.Identifier_reference(value=identifier.value)

        self.raise_unexpected_token()

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

        self.raise_unexpected_token(type_)

    def raise_unexpected_token(self, expected: Token.types = None):
        if expected is not None:
            raise ValueError(
                f"Expected {expected.name} at {self.tokenizer.position}, instead got {self.tokenizer.next.type.name}!"
            )

        raise ValueError(
            f"Unexpected token {self.tokenizer.next.type.name} at {self.tokenizer.position}!"
        )
