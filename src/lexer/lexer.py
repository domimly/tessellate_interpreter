from src.lexer.tokens import Token, TokenType
from src.lexer.stream import TextPosition
from src.error_handling.lexer_error import (
    InvalidSyntaxError,
    IdentifierTooLongError,
    StringTooLongError,
    InvalidEscapeSequenceError,
    UnclosedStringError,
    IntTooBigError,
    TooManyDecimalsInFloatError
)


class Lexer:
    def __init__(
        self, stream, max_id, max_string, max_int, max_float_decimals
    ):
        self.stream = stream
        self.current_token_position = TextPosition(1, 0)
        self.max_id = max_id
        self.max_string = max_string
        self.max_int = max_int
        self.max_float_decimals = max_float_decimals

        self.keywords = {
            'def': TokenType.DEF,
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'return': TokenType.RETURN,

            'and': TokenType.AND_OPERATOR,
            'or': TokenType.OR_OPERATOR,
            'not': TokenType.NEGATION_OPERATOR,

            'True': TokenType.BOOL,
            'False': TokenType.BOOL
        }

        self.escapes = {
            'n': '\n',
            'b': '\b',
            'r': '\r',
            't': '\t',
        }

        self.chars_and_operators = {
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '.': TokenType.POINT,
            '(': TokenType.LEFT_PARENTHASIS,
            ')': TokenType.RIGHT_PARENTHASIS,
            '{': TokenType.LEFT_CURLY_BRACKETS,
            '}': TokenType.RIGHT_CURLY_BRACKETS,
            '[': TokenType.LEFT_SQUARE_BRACKETS,
            ']': TokenType.RIGHT_SQUARE_BRACKETS,

            '+': TokenType.ADD_OPERATOR,
            '-': TokenType.SUBTRACT_OPERATOR,
            '%': TokenType.MODULO_OPERATOR,
        }

        self.long_operators = {
            '&': ('&&', TokenType.AND_OPERATOR),
            '|': ('||', TokenType.OR_OPERATOR),
        }

        self.complex_operators = {
            '/': ('//',
                  TokenType.DIVIDE_OPERATOR,
                  TokenType.FLOOR_DIVIDE_OPERATOR),
            '*': ('**',
                  TokenType.MULTIPLY_OPERATOR,
                  TokenType.POWER_OPERATOR),
            '=': ('==',
                  TokenType.ASSIGN_OPERATOR,
                  TokenType.EQUAL_OPERATOR),
            '!': ('!=',
                  TokenType.NEGATION_OPERATOR,
                  TokenType.NOT_EQUAL_OPERATOR),
            '<': ('<=',
                  TokenType.LESS_THAN_OPERATOR,
                  TokenType.LESS_OR_EQUAL_OPERATOR),
            '>': (">=",
                  TokenType.MORE_THAN_OPERATOR,
                  TokenType.MORE_OR_EQUAL_OPERATOR)
        }

    def current_char(self):
        return self.stream.get_char()

    def next_char(self):
        return self.stream.next_char()

    def current_position(self):
        return self.stream.get_position()

    def set_current_token_position(self):
        self.current_token_position = TextPosition(
            self.current_position().current_line,
            self.current_position().current_column
        )

    def tokenize(self):
        self.skip_whitespace()
        self.set_current_token_position()
        token = (
            self.try_comment() or
            self.try_eof() or
            self.try_identifier_or_keyword() or
            self.try_string() or
            self.try_integer_or_float() or
            self.try_char_or_operator() or
            self.try_long_operator() or
            self.try_complex_operator()
        )
        if token:
            return token
        else:
            raise InvalidSyntaxError(
                self.current_token_position
            )

    def skip_whitespace(self):
        char = self.current_char()
        while char.isspace():
            char = self.next_char()

    def try_comment(self):
        char = self.current_char()
        if char == '#':
            char = self.next_char()
            while (char != '\n'):
                char = self.next_char()
                if char == 'EOF':
                    return
            self.next_char()
            self.set_current_token_position()
            return

    def try_eof(self):
        if self.current_char() == 'EOF':
            return Token(
                TokenType.END_OF_FILE,
                self.current_position()
            )

    def try_identifier_or_keyword(self):
        identifier = ''
        char = self.current_char()
        if char.isalpha():
            i = 1
            identifier += char
            char = self.next_char()
            while ((char.isalnum() or char == '_')
                    and char != 'EOF'):
                i += 1
                if i > self.max_id:
                    raise IdentifierTooLongError(
                        self.max_id,
                        self.current_token_position
                    )
                identifier += char
                char = self.next_char()
            if token_type := self.keywords.get(identifier):
                if identifier == 'True':
                    val = True
                elif identifier == 'False':
                    val = False
                else:
                    val = None
                return Token(
                    token_type,
                    self.current_token_position,
                    val
                )
            else:
                return Token(
                    TokenType.IDENTIFIER,
                    self.current_token_position,
                    identifier
                )

    def try_string(self):
        string = ''
        quote_char = self.current_char()
        if quote_char == '"' or quote_char == "'":
            char = self.next_char()
            i = 0
            while char != quote_char:
                if char == 'EOF' or char == 'NEWLINE':
                    raise UnclosedStringError(
                        self.current_token_position
                    )
                i += 1
                if i > self.max_string:
                    raise StringTooLongError(
                        self.max_string,
                        self.current_token_position
                    )
                if self.current_char() == '\\':
                    char = self.next_char()
                    if char in ['\\', '"', "'"]:
                        string += char
                    elif escaped_char := self.escapes.get(char):
                        string += escaped_char
                    else:
                        raise InvalidEscapeSequenceError(
                            char,
                            self.current_position()
                        )
                else:
                    string += char
                char = self.next_char()
            self.next_char()
            return Token(
                TokenType.STRING,
                self.current_token_position,
                string
            )

    def try_integer_or_float(self):
        number = 0
        char = self.current_char()
        if char.isdigit():
            i = 1
            number += int(char)
            char = self.next_char()
            while char.isdigit():
                i += 1
                if i > self.max_int:
                    raise IntTooBigError(
                        self.max_int,
                        self.current_token_position
                    )
                number = number * 10 + int(char)
                char = self.next_char()
            if char != '.':
                return Token(
                    TokenType.INTEGER,
                    self.current_token_position,
                    number
                )
            char = self.next_char()
            fractional = 0
            divisor = 10
            j = 0
            while char.isdigit():
                j += 1
                if j > self.max_float_decimals:
                    raise TooManyDecimalsInFloatError(
                        self.max_float_decimals,
                        self.current_token_position
                    )
                fractional += int(char) / divisor
                divisor *= 10
                char = self.next_char()
            number = float(number) + fractional
            print(type(number))
            return Token(
                TokenType.FLOAT,
                self.current_token_position,
                number
            )

    def try_char_or_operator(self):
        char = self.current_char()
        if token_type := self.chars_and_operators.get(char):
            self.next_char()
            return Token(
                token_type,
                self.current_token_position
            )

    def try_long_operator(self):
        first_char = self.current_char()
        if token_type := self.long_operators.get(first_char):
            second_char = self.next_char()
            if first_char + second_char == token_type[0]:
                self.next_char()
                return Token(
                    token_type[1],
                    self.current_token_position
                )

    def try_complex_operator(self):
        first_char = self.current_char()
        if token_type_tuple := self.complex_operators.get(first_char):
            second_char = self.next_char()
            if first_char + second_char != token_type_tuple[0]:
                return Token(
                    token_type_tuple[1],
                    self.current_token_position
                )
            else:
                self.next_char()
                return Token(
                    token_type_tuple[2],
                    self.current_token_position
                )
