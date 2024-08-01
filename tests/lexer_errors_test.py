import io

from src.lexer.stream import Stream
from src.lexer.lexer import Lexer
from src.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
    MAXIMUM_FLOAT_DECIMALS
)
from src.lexer.tokens import TokenType
from src.error_handling.lexer_error import (
    LexerError,
    InvalidSyntaxError,
    UnclosedStringError,
    # InvalidEscapeSequenceError,
    IntTooBigError,
    StringTooLongError,
    IdentifierTooLongError,
    # TooManyDecimalsInFloatError
)


class TestLexerErrors:
    def get_tokens(self, lexer):
        tokens = []
        errors = []
        while True:
            try:
                if token := lexer.tokenize():
                    tokens.append(token)
                    if token.token_type == TokenType.END_OF_FILE:
                        break
            except LexerError as e:
                errors.append(e)
                break
        return tokens, errors

    def get_tokens_errors_from_text(self, text):
        lexer = Lexer(
            Stream(io.StringIO(text)),
            MAXIMUM_IDENTIFIER,
            MAXIMUM_STRING,
            MAXIMUM_INT_DIGITS,
            MAXIMUM_FLOAT_DECIMALS
        )
        _, errors = self.get_tokens(lexer)
        error_position = (
            errors[0].position.current_line, errors[0].position.current_column
        )
        return errors[0], error_position

    def test_invalid_token_error(self):
        t = '^'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, InvalidSyntaxError)
        assert error_position == (1, 1)

    def test_invalid_token_error_with_other(self):
        t = 'identifier ^'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, InvalidSyntaxError)
        assert error_position == (1, len(t))

    def test_unclosed_string(self):
        t = '"unclosed string'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, UnclosedStringError)
        assert error_position == (1, 1)

    def test_unmatched_quotes_in_string(self):
        t1 = '"unmatched '
        t2 = "quotes'"
        t = t1 + t2
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, UnclosedStringError)
        assert error_position == (1, 1)

    def test_string_too_long(self):
        string_too_long = "a" * (MAXIMUM_STRING + 1)
        t = f'"{string_too_long}"'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, StringTooLongError)
        assert error_position == (1, 1)

    def test_identifier_too_long(self):
        t = "i" * (MAXIMUM_IDENTIFIER + 1)
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, IdentifierTooLongError)
        assert error_position == (1, 1)

    def test_int_too_big(self):
        t = "9" * (MAXIMUM_INT_DIGITS + 1)
        error, error_position = self.get_tokens_errors_from_text(t)
        assert isinstance(error, IntTooBigError)
        assert error_position == (1, 1)
