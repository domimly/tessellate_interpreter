import argparse

from src.lexer.lexer import Lexer
from src.lexer.stream import Stream
from src.parser.parser import Parser
from src.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
    MAXIMUM_FLOAT_DECIMALS,
    MAXIMUM_RECURSION_DEPTH
)
from src.interpreter.interpreter import Interpreter

PATH = './examples/code_example.txt'


def main(file, max_id, max_string, max_int, max_float_decimals, max_recursion):
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
    interpreter = Interpreter(max_recursion)
    interpreter.interpret(program)


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
    parser.add_argument(
        "--max_recursion_depth",
        type=int,
        help="maximum function recursion depth"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="path to the file containing the code"
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
    max_recursion = (
        args.max_recursion_depth if args.max_recursion_depth
        else MAXIMUM_RECURSION_DEPTH
    )
    file = (
        args.file if args.file
        else PATH
    )

    main(file, max_id, max_string, max_int, max_float_decimals, max_recursion)
