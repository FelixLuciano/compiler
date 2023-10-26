from dataclasses import dataclass, field

import src.nodes as nodes
from src.Pre_processing import Pre_processing
from src.Token import Token
from src.Tokenizer import Tokenizer
from src.Typed_value import Typed_value


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

    def parse_statement(self, endl=True):
        statement = nodes.No_operation()

        if self.check_then_consume(Token.types.VAR_STATEMENT):
            name = self.expect_then_consume(Token.types.IDENTIFIER).value

            statement = nodes.Identifier_declaration(
                value=name,
                children=[
                    nodes.String_value(
                        value=self.expect_then_consume(Token.types.IDENTIFIER).value
                    ),
                ],
            )

            if self.check_then_consume(Token.types.ASSIGNMENT):
                statement.children.append(nodes.Identifier_assignment(
                    value=name,
                    children=[
                        self.parse_expression()
                    ]
                ))
        if self.check_then_consume(Token.types.IF_STATEMENT):
            children = [self.parse_expression(), self.parse_block()]

            if self.check_then_consume(Token.types.ELSE_STATEMENT):
                children.append(self.parse_block())

            statement = nodes.Conditional_block(
                value=None,
                children=children,
            )
        elif self.check_then_consume(Token.types.FOR_STATEMENT):
            assignment = self.parse_expression()
            self.expect_then_consume(Token.types.HARD_SEPARATOR)
            condition = self.parse_expression()
            self.expect_then_consume(Token.types.HARD_SEPARATOR)
            step = self.parse_expression()
            block = self.parse_block()

            statement =  nodes.Iterator_block(
                value=None,
                children=[
                    assignment,
                    condition,
                    step,
                    block,
                ],
            )
        elif not self.check(Token.types.END_OF_LINE):
            statement =  self.parse_expression()

        if self.check_any(Token.types.END_OF_LINE, Token.types.END_OF_FILE):
            self.check_then_consume(Token.types.END_OF_LINE)

        return statement
    
    def parse_expression(self):
        expression = self.parse_boolean_expression()

        if isinstance(expression, nodes.Identifier_reference):
            assign = False
            operation = None

            if self.check_any(Token.types.ASSIGNMENT, Token.types.ASSIGNMENT_PLUS, Token.types.ASSIGNMENT_MINUS, Token.types.ASSIGNMENT_MULT, Token.types.ASSIGNMENT_DIV, Token.types.ASSIGNMENT_MODULO):
                operation = None
                if not self.check(Token.types.ASSIGNMENT):
                    operation = self.get_then_consume().type
                else:
                    self.consume()
                assign = True

                if operation == Token.types.ASSIGNMENT_PLUS:
                    operation = Token.types.OP_PLUS
                elif operation == Token.types.ASSIGNMENT_MINUS:
                    operation = Token.types.OP_MINUS
                elif operation == Token.types.ASSIGNMENT_MULT:
                    operation = Token.types.OP_MULT
                elif operation == Token.types.ASSIGNMENT_DIV:
                    operation = Token.types.OP_DIV
                elif operation == Token.types.ASSIGNMENT_MODULO:
                    operation = Token.types.OP_MODULO

            if assign:
                value = self.parse_expression()

                if operation is not None:
                    value = nodes.Binary_operation(
                        value=operation,
                        children=[
                            expression,
                            value,
                        ]
                    )

                return nodes.Identifier_assignment(
                    value=expression.value,
                    children=[
                        value,
                    ],
                )

        return expression
    
    def parse_boolean_expression(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_boolean_term, Token.types.OP_OR)

    def parse_boolean_term(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_boolean_factor, Token.types.OP_AND)
    
    def parse_boolean_factor(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_arithmetic_expression, Token.types.OP_EQUAL, Token.types.OP_NOT_EQUAL, Token.types.OP_GREATER, Token.types.OP_LOWER, Token.types.OP_GREATER_EQUAL, Token.types.OP_LOWER_EQUAL)

    def parse_arithmetic_expression(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_arithmetic_term, Token.types.OP_PLUS, Token.types.OP_MINUS, Token.types.OP_CONCAT)

    def parse_arithmetic_term(self) -> nodes.Node:
        return self.parse_binary_operation(self.parse_arithmetic_factor, Token.types.OP_MULT, Token.types.OP_DIV)

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

    def parse_arithmetic_factor(self) -> nodes.Node:
        factor = None

        if self.check_then_consume(Token.types.QUOTATION):
            characters = []

            while not(self.check_then_consume(Token.types.QUOTATION)):
                if self.check_any(Token.types.END_OF_LINE, Token.types.END_OF_FILE):
                    self.raise_unexpected_token()

                characters.append(self.get_then_consume().value)

            factor = nodes.String_value(value="".join(characters))
        elif self.check_then_consume(Token.types.OPEN_PARENTHESIS):
            factor = self.parse_boolean_expression()

            self.expect_then_consume(Token.types.CLOSE_PARENTHESIS)
        elif self.check(Token.types.NUMBER):
            factor =  nodes.Integer_value(value=self.get_then_consume().value)
        elif self.check(Token.types.IDENTIFIER):
            factor = nodes.Identifier_reference(value=self.get_then_consume().value)

            if self.check(Token.types.OPEN_PARENTHESIS):
                factor = self.parse_call(factor)
        elif self.check_any(Token.types.OP_PLUS, Token.types.OP_MINUS, Token.types.OP_NOT):
            factor = nodes.Unary_operation(
                value=self.get_then_consume().type,
                children=[self.parse_arithmetic_factor()]
            )

        if factor is not None:
            if self.check_then_consume(Token.types.OP_NOT):
                if isinstance(factor, nodes.Binary_operation):
                    factor.children[1] = nodes.Unary_operation(
                        value=Token.types.OP_FATORIAL,
                        children=[factor.children[1]]
                    )
                else:
                    factor = nodes.Unary_operation(
                        value=Token.types.OP_FATORIAL,
                        children=[factor]
                    )
            elif self.check_any(Token.types.OP_POWER, Token.types.OP_MODULO):
                factor = nodes.Binary_operation(
                    value=self.get_then_consume().type,
                    children=[factor, self.parse_arithmetic_factor()]
                )

            return factor

        return self.raise_unexpected_token()

    def parse_call(self, reference: nodes.Identifier_reference) -> nodes.Identifier_call:
        self.expect_then_consume(Token.types.OPEN_PARENTHESIS)

        arguments = []

        if not self.check(Token.types.CLOSE_PARENTHESIS):
            arguments.append(self.parse_boolean_expression())

        while self.check_then_consume(Token.types.SEPARATOR):
            arguments.append(self.parse_boolean_expression())

        self.expect_then_consume(Token.types.CLOSE_PARENTHESIS)

        return nodes.Identifier_call(
            value=reference.value,
            children=arguments,
        )

    def parse_block(self) -> nodes.Block:
        statements = []

        self.expect_then_consume(Token.types.OPEN_BRACES)
        self.expect_then_consume(Token.types.END_OF_LINE)

        while not self.check_then_consume(Token.types.CLOSE_BRACES):
            statements.append(self.parse_statement())

        return nodes.Block(None, statements)

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
        if self.check(type_):
            return self.get_then_consume()

        return self.raise_unexpected_token(type_)

    def raise_unexpected_token(self, expected: Token.types = None):
        if expected is not None:
            raise ValueError(
                f"Expected {expected.name} at {self.tokenizer.position}, instead got {self.tokenizer.next.type.name}!"
            )

        raise ValueError(
            f"Unexpected token {self.tokenizer.next.type.name} at {self.tokenizer.position}!"
        )
