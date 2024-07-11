import io

from lexer.stream import Stream
from lexer.lexer import Lexer
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


class TestLexerErrors:
    def get_tokens_errors_from_text(self, text):
        lexer = Lexer(Stream(io.StringIO(text)))
        _, errors = lexer.get_tokens()
        error_position = (
            errors[0].position.current_line, errors[0].position.current_column
        )
        return errors[0], error_position

    def test_invalid_token_error(self):
        t = '^'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == INVALID_SYNTAX_ERROR_MSG
        assert error_position == (1, 1)

    def test_invalid_token_error_with_other(self):
        t = 'identifier ^'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == INVALID_SYNTAX_ERROR_MSG
        assert error_position == (1, len(t))

    def test_unclosed_string(self):
        t = '"unclosed string'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == UNCLOSED_STRING_ERROR_MSG
        assert error_position == (1, 1)

    def test_unmatched_quotes_in_string(self):
        t1 = '"unmatched '
        t2 = "quotes'"
        t = t1 + t2
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == UNCLOSED_STRING_ERROR_MSG
        assert error_position == (1, 1)

    def test_string_too_long(self):
        string_too_long = "a" * (MAXIMUM_STRING + 1)
        t = f'"{string_too_long}"'
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == STRING_TOO_LONG_ERROR_MSG
        assert error_position == (1, 1)

    def test_identifier_too_long(self):
        t = "i" * (MAXIMUM_IDENTIFIER + 1)
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == IDENTIFIER_TOO_LONG_ERROR_MSG
        assert error_position == (1, 1)

    def test_int_too_big(self):
        t = "9" * (MAXIMUM_INT_DIGITS + 1)
        error, error_position = self.get_tokens_errors_from_text(t)
        assert error.message == INT_TOO_BIG_ERROR_MSG
        assert error_position == (1, 1)
