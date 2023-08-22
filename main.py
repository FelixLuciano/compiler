import argparse

from src.Parser import Parser


def main(args: argparse.Namespace):
    print(Parser.run(args.expression))


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("expression", help="Sum expression. Eg.: \"1 + 1\"")

    main(args.parse_args())
