import string
import argparse


def main(args: argparse.Namespace):
    answer: int = 0
    current = 0
    operation = 1
    is_empty: bool = True

    if len(args.expression) < 1:
        raise ValueError("Cannot read empty expressions!")

    for index, char in enumerate(args.expression):
        if is_empty and char in ("-", "+"):
            raise ValueError(f"Invalid token at {index}!")
        elif char in string.digits:
            is_empty = False
            current = 10 * current + int(char)
        elif char == "+":
            answer += current * operation
            current = 0
            operation = 1
        elif char == "-":
            answer += current * operation
            current = 0
            operation = -1
        elif char in string.whitespace:
            continue
        else:
            raise ValueError(f"Invalid token at {index}!")
        
    answer += current * operation
        
    print(answer)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("expression", help="Sum expression. Eg.: \"1 + 1\"")

    main(args.parse_args())
