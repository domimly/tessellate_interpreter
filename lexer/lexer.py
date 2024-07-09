from lexer.tokens import Token, TokenType
from lexer.stream import TextPosition
from lexer.lexer_error import LexerError
from lexer.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
    INVALID_SYNTAX_ERROR_MSG,
    IDENTIFIER_TOO_LONG_ERROR_MSG,
    STRING_TOO_LONG_ERROR_MSG,
    UNCLOSED_STRING_ERROR_MSG,
    INT_TOO_BIG_ERROR_MSG
)


class Lexer:
    def __init__(self, stream):
        self.stream = stream
        self.current_token_position = TextPosition(1, 0)

        self.keywords = {
            'def': TokenType.DEF,
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'return': TokenType.RETURN,

            'and': TokenType.AND_OPERATOR,
            'or': TokenType.OR_OPERATOR,
            'not': TokenType.NEGATION_OPERATOR,

            'True': TokenType.BOOL,
            'False': TokenType.BOOL
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

    def next_string_char(self):
        return self.stream.next_string_char()

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
            raise LexerError(
                INVALID_SYNTAX_ERROR_MSG,
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
            self.skip_comment()

    def skip_comment(self):
        char = self.current_char()
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
                '',
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
                if i > MAXIMUM_IDENTIFIER:
                    raise LexerError(
                        IDENTIFIER_TOO_LONG_ERROR_MSG,
                        self.current_token_position
                    )
                identifier += char
                char = self.next_char()
            if token_type := self.keywords.get(identifier):
                if identifier in ['True', 'False']:
                    val = identifier
                else:
                    val = ''
                return Token(
                    token_type,
                    val,
                    self.current_token_position
                )
            else:
                return Token(
                    TokenType.IDENTIFIER,
                    identifier,
                    self.current_token_position
                )

    def try_string(self):
        string = ''
        quote_char = self.current_char()
        if quote_char == '"' or quote_char == "'":
            char = self.next_string_char()
            i = 0
            while char != quote_char:
                if char == 'EOF':
                    raise LexerError(
                        UNCLOSED_STRING_ERROR_MSG,
                        self.current_token_position
                    )
                i += 1
                if i > MAXIMUM_STRING:
                    raise LexerError(
                        STRING_TOO_LONG_ERROR_MSG,
                        self.current_token_position
                    )
                string += char
                char = self.next_string_char()
            self.next_char()
            return Token(
                TokenType.STRING,
                string,
                self.current_token_position
            )

    def try_integer_or_float(self):
        number = ''
        char = self.current_char()
        if char.isdigit():
            i = 1
            number += char
            char = self.next_char()
            while char.isdigit():
                i += 1
                if i > MAXIMUM_INT_DIGITS:
                    raise LexerError(
                        INT_TOO_BIG_ERROR_MSG,
                        self.current_token_position
                    )
                number += char
                char = self.next_char()
            if char != '.':
                return Token(
                    TokenType.INTEGER,
                    int(number),
                    self.current_token_position
                )
            number += char
            char = self.next_char()
            while char.isdigit():
                number += char
                char = self.next_char()
            return Token(
                TokenType.FLOAT,
                float(number),
                self.current_token_position
            )

    def try_char_or_operator(self):
        char = self.current_char()
        if token_type := self.chars_and_operators.get(char):
            self.next_char()
            return Token(
                token_type,
                '',
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
                    '',
                    self.current_token_position
                )

    def try_complex_operator(self):
        first_char = self.current_char()
        if token_type_tuple := self.complex_operators.get(first_char):
            second_char = self.next_char()
            if first_char + second_char != token_type_tuple[0]:
                return Token(
                    token_type_tuple[1],
                    '',
                    self.current_token_position
                )
            else:
                self.next_char()
                return Token(
                    token_type_tuple[2],
                    '',
                    self.current_token_position
                )

    def get_tokens(self):
        tokens = []
        errors = []
        while True:
            try:
                if token := self.tokenize():
                    tokens.append(token)
                    if token.token_type == TokenType.END_OF_FILE:
                        break
            except LexerError as e:
                errors.append(e)
                break
        return tokens, errors
