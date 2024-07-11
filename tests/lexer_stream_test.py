from lexer.stream import Stream
from lexer.lexer import Lexer
from lexer.tokens import TokenType

from lexer.constants import (
    INVALID_SYNTAX_ERROR_MSG,
    UNCLOSED_STRING_ERROR_MSG,
)

PATH = 'tests/code_examples/'


class TestLexerStream:
    def get_tokens_info_from_stream(self, path):
        with open(path, 'r') as file:
            lexer = Lexer(Stream(file))
            tokens, errors = lexer.get_tokens()
        tokens_types = []
        tokens_values = []
        tokens_positions = []
        for token in tokens:
            tokens_types.append(token.token_type)
            tokens_values.append(token.value)
            tokens_positions.append(
                (token.position.current_line, token.position.current_column)
            )
        return tokens_types, tokens_values, tokens_positions, errors

    def get_error_info(self, errors):
        if errors[0]:
            error_position = (
                errors[0].position.current_line,
                errors[0].position.current_column
            )
            return errors[0], error_position

    def test_example(self):

        # pi = 3.14;
        # name = "Name";
        #
        # num = 100;

        path = PATH + 'example.txt'
        (types, values, positions, errors) = (
            self.get_tokens_info_from_stream(path)
        )
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.FLOAT,
            TokenType.SEMICOLON,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.STRING,
            TokenType.SEMICOLON,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.INTEGER,
            TokenType.SEMICOLON,
            TokenType.END_OF_FILE
        ]
        assert (values) == [
            'pi', '', 3.14, '',
            'name', '', 'Name', '',
            'num', '', 100, '', ''
        ]
        assert positions == [
            (1, 1), (1, 4), (1, 6), (1, 10),
            (2, 1), (2, 6), (2, 8), (2, 14),
            (4, 1), (4, 5), (4, 7), (4, 10), (4, 11)
        ]
        assert len(errors) == 0

    def test_all_token_types(self):
        path = PATH + 'all_types.txt'
        (types, values, _, errors) = (
            self.get_tokens_info_from_stream(path)
        )
        assert types == [
            # characters
            TokenType.SEMICOLON,
            TokenType.COMMA,
            TokenType.POINT,
            TokenType.LEFT_PARENTHASIS,
            TokenType.RIGHT_PARENTHASIS,
            TokenType.LEFT_CURLY_BRACKETS,
            TokenType.RIGHT_CURLY_BRACKETS,
            TokenType.LEFT_SQUARE_BRACKETS,
            TokenType.RIGHT_SQUARE_BRACKETS,

            # operators
            TokenType.ASSIGN_OPERATOR,
            TokenType.ADD_OPERATOR,
            TokenType.SUBTRACT_OPERATOR,
            TokenType.MULTIPLY_OPERATOR,
            TokenType.DIVIDE_OPERATOR,
            TokenType.FLOOR_DIVIDE_OPERATOR,
            TokenType.MODULO_OPERATOR,
            TokenType.POWER_OPERATOR,
            TokenType.AND_OPERATOR,
            TokenType.OR_OPERATOR,
            TokenType.EQUAL_OPERATOR,
            TokenType.NOT_EQUAL_OPERATOR,
            TokenType.LESS_THAN_OPERATOR,
            TokenType.LESS_OR_EQUAL_OPERATOR,
            TokenType.MORE_THAN_OPERATOR,
            TokenType.MORE_OR_EQUAL_OPERATOR,
            TokenType.NEGATION_OPERATOR,

            # data types
            TokenType.INTEGER,
            TokenType.FLOAT,
            TokenType.BOOL,
            TokenType.STRING,

            # keywords
            TokenType.DEF,
            TokenType.IF,
            TokenType.ELIF,
            TokenType.ELSE,
            TokenType.FOR,
            TokenType.WHILE,
            TokenType.BREAK,
            TokenType.RETURN,

            # other
            TokenType.IDENTIFIER,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {'', 1, 1.1, 'True', 'string', 'identifier'}
        assert len(errors) == 0

    def test_comments(self):

        # i = 1;    # comment 1
        # j = True; # comment 2

        path = PATH + 'comments.txt'
        (types, values, positions, errors) = (
            self.get_tokens_info_from_stream(path)
        )
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.INTEGER,
            TokenType.SEMICOLON,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.BOOL,
            TokenType.SEMICOLON,
            TokenType.END_OF_FILE
        ]
        assert (values) == [
            'i', '', 1, '',
            'j', '', 'True', '', ''
        ]
        assert positions == [
            (1, 1), (1, 3), (1, 5), (1, 6),
            (2, 1), (2, 3), (2, 5), (2, 9),
            (2, len('j = True; # comment 2') + 1)
        ]
        assert len(errors) == 0

    def test_invalid_syntax(self):

        # i=3;
        # j=_;

        path = PATH + 'invalid_syntax.txt'
        (types, values, positions, errors) = (
            self.get_tokens_info_from_stream(path)
        )
        error, error_position = self.get_error_info(errors)
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
            TokenType.INTEGER,
            TokenType.SEMICOLON,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
        ]
        assert (values) == [
            'i', '', 3, '',
            'j', ''
        ]
        assert positions == [
            (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 2)
        ]
        assert error.message == INVALID_SYNTAX_ERROR_MSG
        assert error_position == (2, 3)

    def test_unclosed_string(self):

        # s = "Unclosed string

        path = PATH + 'unclosed_string.txt'
        (types, values, positions, errors) = (
            self.get_tokens_info_from_stream(path)
        )
        error, error_position = self.get_error_info(errors)
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OPERATOR,
        ]
        assert (values) == [
            's', ''
        ]
        assert positions == [
            (1, 1), (1, 3)
        ]
        assert error.message == UNCLOSED_STRING_ERROR_MSG
        assert error_position == (1, 5)
