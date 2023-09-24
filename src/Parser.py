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

        if tokenizer.next.type != Token.types.END_OF_FILE:
            raise ValueError(f'Invalid expression "{code}"')

        return answer

    def parse_block(self) -> Block_node:
        statements = []

        while not self._check_next_for(Token.types.END_OF_FILE):
            statement = self.parse_statement()

            statements.append(statement)

        return Block_node(None, statements)

    def parse_statement(self):
        statement = No_operation_node

        if self._check_next_for(Token.types.IDENTIFIER):
            identifier = self.tokenizer.next

            self._consume_token()

            if self._check_next_for(Token.types.ASSIGNMENT):
                self._consume_token()

                statement = Identifier_assignment_node(identifier.value, [self.parse_expression()])
            elif self._check_next_for(Token.types.OPEN_PARENTHESIS):
                self._consume_token()

                arguments = []

                while not self._check_next_for(Token.types.CLOSE_PARENTHESIS):
                    expression = self.parse_expression()

                    if self._check_next_for(Token.types.SEPARATOR):
                        self._consume_token()
                    elif self._check_next_for(Token.types.END_OF_LINE):
                        raise ValueError(
                            f"Expected , or ) after expression at {self.tokenizer.position}!"
                        )

                    arguments.append(expression)

                self._consume_token()
        
                statement = Identifier_call_node(identifier.value, arguments)

        if not self._check_next_for(Token.types.END_OF_LINE):
            raise ValueError(
                f"Expected new line after statement at {self.tokenizer.position}!"
            )
        
        self._consume_token()

        return statement

    def parse_expression(self) -> Abstract_node:
        root = self.parse_term()

        while True:
            if self._check_next_for(Token.types.OP_PLUS):
                operator = Token.types.OP_PLUS
            elif self._check_next_for(Token.types.OP_MINUS):
                operator = Token.types.OP_MINUS
            else:
                break

            self._consume_token()

            next = self.parse_term()

            if operator == Token.types.OP_PLUS:
                root = Binary_operation_node(Token.types.OP_PLUS, [root, next])
            elif operator == Token.types.OP_MINUS:
                root = Binary_operation_node(Token.types.OP_MINUS, [root, next])

        return root

    def parse_term(self) -> Abstract_node:
        root = self.parse_factor()

        while True:
            if self._check_next_for(Token.types.OP_MULT):
                operator = Token.types.OP_MULT
            elif self._check_next_for(Token.types.OP_DIV):
                operator = Token.types.OP_DIV
            else:
                break

            self._consume_token()

            if operator == Token.types.OP_MULT:
                root = Binary_operation_node(Token.types.OP_MULT, [root, self.parse_factor()])
            elif operator == Token.types.OP_DIV:
                root = Binary_operation_node(Token.types.OP_DIV, [root, self.parse_factor()])

        return root
    
    def parse_factor(self):
        if self._check_next_for(Token.types.NUMBER):
            value = self.tokenizer.next.value
            
            self._consume_token()

            return Integer_value_node(value)
        if self._check_next_for(Token.types.IDENTIFIER):
            value = self.tokenizer.next.value
            
            self._consume_token()

            return Identifier_reference_node(value)
        elif self._check_next_for(Token.types.OP_PLUS):
            self._consume_token()
            return Unary_operation_node(Token.types.OP_PLUS, [self.parse_factor()])
        elif self._check_next_for(Token.types.OP_MINUS):
            self._consume_token()
            return Unary_operation_node(Token.types.OP_MINUS, [self.parse_factor()])
        elif self._check_next_for(Token.types.OPEN_PARENTHESIS):
            self._consume_token()

            expression = self.parse_expression()

            if not self._check_next_for(Token.types.CLOSE_PARENTHESIS):
                raise ValueError(
                    f"Expected ) after expression at {self.tokenizer.position}!"
                )

            self._consume_token()

            return expression
    
    def _check_next_for(self, type_: Token.types):
        return self.tokenizer.next.check(type_)
    
    def _consume_token(self):
        print("CONSUME", self.tokenizer.next.type.name)
        return self.tokenizer.select_next()
