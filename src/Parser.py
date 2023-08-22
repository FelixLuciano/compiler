from dataclasses import dataclass, field

from src.Token import Token
from src.Tokenizer import Tokenizer


@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    def parseExpression():
        pass

    @staticmethod
    def run(code: str):
        def initialize_tokenizer():
            try:
                tokenizer = Tokenizer(code)

                if tokenizer.next.type != Token.types.NUMBER.name:
                    raise Parser.ParseError(code, (0, 1), f"Invalid token at {tokenizer.position}. {tokenizer.next.type} is not an valid initializer!")
            
                return tokenizer
            except AttributeError as error:
                raise Parser.ParseError(code, (0, 1), f"Invalid token at 0. {error.args[0]}")
            
        def selectNext(tokenizer: Tokenizer):
            try:
                return tokenizer.selectNext()
            except AttributeError as error:
                raise Parser.ParseError(code, (1, 1), f"Invalid token at 1. {error.args[0]}")

        tokenizer = initialize_tokenizer()
        next = selectNext(tokenizer)

        answer = next.value

        while True:
            prev = next
            next = selectNext(tokenizer)

            if prev.type == next.type:
                raise Parser.ParseError(code, (tokenizer.position, 1), f"Invalid token at {tokenizer.position}. There couldn't be simultaneous tokens!")
            elif next.type == Token.types.EOS.name:
                if prev.type != Token.types.NUMBER.name:
                    raise Parser.ParseError(code, (tokenizer.position, 1), f"Expected a {Token.types.NUMBER.name} after a {prev.type} at {tokenizer.position}!")
                break
            elif next.type == Token.types.NUMBER.name:
                if prev.type == Token.types.PLUS.name:
                    answer += next.value
                elif prev.type == Token.types.MINUS.name:
                    answer -= next.value
                else:
                    raise Parser.ParseError(code, (tokenizer.position, 1), f"Invalid operation at {tokenizer.position}")

        return answer
    
    class ParseError(Exception):
        def __init__(self, code: str, slice, message: str):
            print(f"{self.__class__.__qualname__}: {message}")
            print(code)
            print((" "*slice[0]) + ("^"*slice[1]))
            exit(0)
