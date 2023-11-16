from pathlib import Path
import argparse

from src.Parser import Parser
from src.Program import Program
from src.SymbolTable import SymbolTable


def main(args: argparse.Namespace):
    filename = Path(args.entry).with_suffix(".asm")

    with open(args.entry, "r") as entry:
        code = entry.read()

    context = SymbolTable()
    program = Program(filename)
    expression = Parser.run(code)

    program.build_header()
    expression.evaluate(context, program)
    program.build_footer()


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("entry", help='Program entry file. Eg.: "main.go"')

    main(args.parse_args())
