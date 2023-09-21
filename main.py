import argparse

from src.Parser import Parser
from src.SymbolTable import SymbolTable


def main(args: argparse.Namespace):
    with open(args.entry, "r") as entry:
        code = entry.read()

    expression = Parser.run(code)
    context = SymbolTable()

    expression.evaluate(context)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("entry", help='Program entry file. Eg.: "main.go"')

    main(args.parse_args())
