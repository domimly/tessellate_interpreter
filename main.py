# import io
import argparse

from src.lexer.lexer import Lexer
from src.lexer.stream import Stream
from src.parser.parser import Parser
from src.parser.print_tree_visitor import PrintTreeVisitor
from src.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
    MAXIMUM_FLOAT_DECIMALS
)

PATH = './examples/code_example.txt'


def main(file, max_id, max_string, max_int, max_float_decimals):
    with open(file, 'r') as f:
        lexer = Lexer(
            Stream(f),
            max_id,
            max_string,
            max_int,
            max_float_decimals
        )
        parser = Parser(lexer)
        program = parser.parse_program()
    printer = PrintTreeVisitor()
    printer.visit(program)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--max_id",
        type=int,
        help="maximum length of an identifier"
    )
    parser.add_argument(
        "--max_string",
        type=int,
        help="maximum length of a string"
    )
    parser.add_argument(
        "--max_int",
        type=int,
        help="maximum integer"
    )
    parser.add_argument(
        "--max_float_decimals",
        type=int,
        help="maximum number of digits after a decimal in float"
    )

    args = parser.parse_args()

    max_id = (
        args.max_id if args.max_id
        else MAXIMUM_IDENTIFIER
    )
    max_string = (
        args.max_string if args.max_string
        else MAXIMUM_STRING
    )
    max_int = (
        args.max_int if args.max_int
        else MAXIMUM_INT_DIGITS
    )
    max_float_decimals = (
        args.max_float_decimals if args.max_float_decimals
        else MAXIMUM_FLOAT_DECIMALS
    )

    main(PATH, max_id, max_string, max_int, max_float_decimals)
