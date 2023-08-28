from dataclasses import dataclass, field

from src.Token import Token
from src.Tokenizer import Tokenizer


@dataclass
class Parser:
    tokenizer: Tokenizer = field()

    def parse_expression(self) -> int:
        answer = self.parse_term()

        print(True, answer)

        while True:
            try:
                self.tokenizer.select_next(Token.types.PLUS)
                answer += self.parse_term()
            except ValueError:
                self.tokenizer.select_next(Token.types.MINUS)
                answer -= self.parse_term()
            except ValueError:
                self.tokenizer.select_next(Token.types.EOF)
                break
            except:
                print("AAAAAAAaaa")

        return answer

    def parse_term(self) -> int:
        answer = self.tokenize.select_next(Token.types.NUMBER.name).value

        while True:
            try:
                self.tokenizer.select_next(Token.types.MULT)
                answer *= self.tokenizer.select_next(Token.types.NUMBER).value
            except ValueError:
                self.tokenizer.select_next(Token.types.DIV)
                answer //= self.tokenizer.select_next(Token.types.NUMBER).value
            except Exception:
                break

        return answer

    @staticmethod
    def run(code: str) -> int:
        return Parser(Tokenizer(code)).parse_expression()

