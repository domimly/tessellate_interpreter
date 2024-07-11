import io

from lexer.stream import Stream
from lexer.lexer import Lexer
from lexer.tokens import TokenType
from lexer.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
)


class TestLexerTokens:
    def get_tokens_info_from_text(self, text):
        lexer = Lexer(Stream(io.StringIO(text)))
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

    def test_eof(self):
        (types, values, positions, errors) = self.get_tokens_info_from_text('')
        assert types == [TokenType.END_OF_FILE]
        assert values == ['']
        assert positions == [(1, 1)]
        assert len(errors) == 0

    def test_characters(self):
        t = ';,.(){}[]'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.SEMICOLON,
            TokenType.COMMA,
            TokenType.POINT,
            TokenType.LEFT_PARENTHASIS,
            TokenType.RIGHT_PARENTHASIS,
            TokenType.LEFT_CURLY_BRACKETS,
            TokenType.RIGHT_CURLY_BRACKETS,
            TokenType.LEFT_SQUARE_BRACKETS,
            TokenType.RIGHT_SQUARE_BRACKETS,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {''}
        assert positions == [
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8),
            (1, 9),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_simple_operators(self):
        t = '+ - %'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.ADD_OPERATOR,
            TokenType.SUBTRACT_OPERATOR,
            TokenType.MODULO_OPERATOR,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {''}
        assert positions == [
            (1, 1),
            (1, 3),
            (1, 5),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_long_operators(self):
        t = '&& ||'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.AND_OPERATOR,
            TokenType.OR_OPERATOR,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {''}
        assert positions == [
            (1, 1),
            (1, 4),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_complex_operators(self):
        t = '/ // * ** = == ! != < <= > >='
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.DIVIDE_OPERATOR,
            TokenType.FLOOR_DIVIDE_OPERATOR,
            TokenType.MULTIPLY_OPERATOR,
            TokenType.POWER_OPERATOR,
            TokenType.ASSIGN_OPERATOR,
            TokenType.EQUAL_OPERATOR,
            TokenType.NEGATION_OPERATOR,
            TokenType.NOT_EQUAL_OPERATOR,
            TokenType.LESS_THAN_OPERATOR,
            TokenType.LESS_OR_EQUAL_OPERATOR,
            TokenType.MORE_THAN_OPERATOR,
            TokenType.MORE_OR_EQUAL_OPERATOR,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {''}
        assert positions == [
            (1, 1),
            (1, 3),
            (1, 6),
            (1, 8),
            (1, 11),
            (1, 13),
            (1, 16),
            (1, 18),
            (1, 21),
            (1, 23),
            (1, 26),
            (1, 28),
            (1, len(t) + 1)

        ]
        assert len(errors) == 0

    def test_keywords(self):
        t = 'def if elif else for while break return and or not True False'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.DEF,
            TokenType.IF,
            TokenType.ELIF,
            TokenType.ELSE,
            TokenType.FOR,
            TokenType.WHILE,
            TokenType.BREAK,
            TokenType.RETURN,
            TokenType.AND_OPERATOR,
            TokenType.OR_OPERATOR,
            TokenType.NEGATION_OPERATOR,
            TokenType.BOOL,
            TokenType.BOOL,
            TokenType.END_OF_FILE
        ]
        assert set(values) == {'', 'True', 'False'}
        assert positions == [
            (1, 1),
            (1, 5),
            (1, 8),
            (1, 13),
            (1, 18),
            (1, 22),
            (1, 28),
            (1, 34),
            (1, 41),
            (1, 45),
            (1, 48),
            (1, 52),
            (1, 57),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_bool(self):
        t = 'True False'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.BOOL,
            TokenType.BOOL,
            TokenType.END_OF_FILE
        ]
        assert values == [
            'True',
            'False',
            ''
        ]
        assert positions == [
            (1, 1),
            (1, 6),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_identifiers(self):
        t = 'identifier identifier2 identifier_3'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.IDENTIFIER,
            TokenType.IDENTIFIER,
            TokenType.END_OF_FILE
        ]
        assert values == [
            'identifier',
            'identifier2',
            'identifier_3',
            ''
        ]
        assert positions == [
            (1, 1),
            (1, 12),
            (1, 24),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_maximum_length_identifier(self):
        t = "i" * MAXIMUM_IDENTIFIER
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.END_OF_FILE
        ]
        assert values == [
            t,
            ''
        ]
        assert positions == [
            (1, 1),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_integers(self):
        t = '125 9 04'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.INTEGER,
            TokenType.INTEGER,
            TokenType.INTEGER,
            TokenType.END_OF_FILE
        ]
        assert values == [
            125,
            9,
            4,
            ''
        ]
        assert positions == [
            (1, 1),
            (1, 5),
            (1, 7),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_maximum_int(self):
        t = "9" * MAXIMUM_INT_DIGITS
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.INTEGER,
            TokenType.END_OF_FILE
        ]
        assert values == [
            int(t),
            ''
        ]
        assert positions == [
            (1, 1),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_floats(self):
        t = '3.14 02.05 999.'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.FLOAT,
            TokenType.FLOAT,
            TokenType.FLOAT,
            TokenType.END_OF_FILE
        ]
        assert values == [
            3.14,
            2.05,
            999.0,
            ''
        ]
        assert positions == [
            (1, 1),
            (1, 6),
            (1, 12),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_string(self):
        t = '"a string\n"'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.STRING,
            TokenType.END_OF_FILE
        ]
        assert values == [
            'a string\n',
            ''
        ]
        assert positions == [
            (1, 1),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_maximum_length_string(self):
        max_string = "a" * MAXIMUM_STRING
        t = f'"{max_string}"'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.STRING,
            TokenType.END_OF_FILE
        ]
        assert values == [
            max_string,
            ''
        ]
        assert positions == [
            (1, 1),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_comment(self):
        t = '# this is a comment'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.END_OF_FILE
        ]
        assert values == [
            ''
        ]
        assert positions == [
            (1, len(t) + 1)
        ]
        assert len(errors) == 0

    def test_comment_with_other(self):
        t = 'this_is_an_identifier # this is a comment'
        (types, values, positions, errors) = self.get_tokens_info_from_text(t)
        assert types == [
            TokenType.IDENTIFIER,
            TokenType.END_OF_FILE
        ]
        assert values == [
            'this_is_an_identifier',
            ''
        ]
        assert positions == [
            (1, 1),
            (1, len(t) + 1)
        ]
        assert len(errors) == 0
