import pytest

from src.lexer.tokens import Token, TokenType
from src.lexer.stream import TextPosition
from src.parser.parser import Parser
from src.error_handling.parser_error import (
    UnexpectedTokenError,
    InvalidSyntaxError
)

from src.parser.parser_tree import (
    Term,
    TermType,
    Identifier,
    ListIndexAccess,
    FunCall,
    DotAccess,
    NotExpressionLogical,
    NotExpressionAritmetic,
    PowerExpression,
    MultiplicationExpression,
    DivisionExpression,
    AdditionExpression,
    SubtractionExpression,
    OperationBlock,
    FunctionDefinition,
    VariableAssignment,
    ListIndex,
    ReturnStatement,
    BreakStatement
)

import unittest


class MockLexer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_position = TextPosition(1, 0)
        self.index = 0

    def tokenize(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token


POS = TextPosition(1, 0)


class TestParser(unittest.TestCase):
    def test_parse_program(self):
        tokens = [
            Token(TokenType.DEF, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'func'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.RETURN, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.RIGHT_CURLY_BRACKETS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(program.statements[0], FunctionDefinition)
        self.assertEqual(program.statements[0].identifier, 'func')
        self.assertEqual(len(program.statements[0].parameters), 0)
        self.assertIsInstance(program.statements[0].body, OperationBlock)
        self.assertEqual(len(program.statements[0].body.statements), 1)
        self.assertIsInstance(
            program.statements[0].body.statements[0], ReturnStatement
        )
        self.assertIsNotNone(program.statements[0].body.statements[0].value)
        self.assertEqual(
            program.statements[0].body.statements[0].position, [1, 0]
        )

    def test_parse_break_statement(self):
        tokens = [
            Token(TokenType.BREAK, POS, None),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        stmt = parser.parse_break_statement()

        self.assertIsNotNone(stmt)
        self.assertIsInstance(stmt, BreakStatement)
        self.assertEqual(stmt.position, [1, 0])

    def test_parse_return_statement_with_expression(self):
        tokens = [
            Token(TokenType.RETURN, POS, None),
            Token(TokenType.INTEGER, POS, 42),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        stmt = parser.parse_return_statement()

        self.assertIsNotNone(stmt)
        self.assertIsInstance(stmt, ReturnStatement)
        self.assertEqual(stmt.position, [1, 0])
        self.assertIsNotNone(stmt.value)
        self.assertEqual(stmt.value.value, 42)

    def test_parse_return_statement_without_expression(self):
        tokens = [
            Token(TokenType.RETURN, POS, None),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        stmt = parser.parse_return_statement()

        self.assertIsNotNone(stmt)
        self.assertIsInstance(stmt, ReturnStatement)
        self.assertEqual(stmt.position, [1, 0])
        self.assertIsNone(stmt.value)

    def test_parse_integer(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 420),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_term()

        self.assertIsInstance(val, Term)
        self.assertEqual(val.value, 420)
        self.assertEqual(val.term_type, TermType.INT)

    def test_parse_float(self):
        tokens = [
            Token(TokenType.FLOAT, POS, 3.14),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_term()

        self.assertIsInstance(val, Term)
        self.assertEqual(val.value, 3.14)
        self.assertEqual(val.term_type, TermType.FLOAT)

    def test_parse_string(self):
        tokens = [
            Token(TokenType.STRING, POS, 'hello'),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_term()

        self.assertIsInstance(val, Term)
        self.assertEqual(val.value, 'hello')
        self.assertEqual(val.term_type, TermType.STRING)

    def test_parse_bool_true(self):
        tokens = [
            Token(TokenType.BOOL, POS, True),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_term()

        self.assertIsInstance(val, Term)
        self.assertIn(val.value, [True])
        self.assertEqual(val.term_type, TermType.BOOL)

    def test_parse_bool_false(self):
        tokens = [
            Token(TokenType.BOOL, POS, False),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_term()

        self.assertIsInstance(val, Term)
        self.assertIn(val.value, [False])
        self.assertEqual(val.term_type, TermType.BOOL)

    def test_parse_single_object(self):
        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'identifier'),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_single_object()

        self.assertIsInstance(val, Identifier)
        self.assertEqual(val.identifier, 'identifier')

    def test_parse_object_with_params(self):
        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'func'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'a'),
            Token(TokenType.COMMA, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'b'),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_single_object()

        self.assertIsInstance(val, FunCall)
        self.assertEqual(val.identifier, 'func')
        self.assertEqual(len(val.arguments), 2)

    def test_parse_object_with_list_index(self):
        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'object'),
            Token(TokenType.LEFT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.RIGHT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_single_object()

        self.assertIsInstance(val, ListIndexAccess)
        self.assertEqual(val.identifier, 'object')
        self.assertEqual(len(val.list_indexes), 1)
        self.assertIsInstance(val.list_indexes[0], ListIndex)
        self.assertEqual(val.list_indexes[0].list_index.value, 1)

    def test_parse_object(self):
        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'object'),
            Token(TokenType.POINT, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'attribute'),
            Token(TokenType.POINT, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'method'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_object()

        self.assertIsInstance(val, DotAccess)
        self.assertIsInstance(val.obj, Identifier)
        self.assertEqual(len(val.dot_access), 2)
        self.assertEqual(val.obj.identifier, 'object')
        self.assertIsInstance(val.dot_access[0], Identifier)
        self.assertEqual(val.dot_access[0].identifier, 'attribute')
        self.assertIsInstance(val.dot_access[1], FunCall)
        self.assertEqual(val.dot_access[1].identifier, 'method')
        self.assertEqual(len(val.dot_access[1].arguments), 0)

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'object'),
            Token(TokenType.LEFT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.RIGHT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.POINT, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'method'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_object()

        self.assertIsInstance(val, DotAccess)
        self.assertEqual(len(val.dot_access), 1)
        self.assertIsInstance(val.obj, ListIndexAccess)
        self.assertEqual(val.obj.identifier, 'object')
        self.assertIsInstance(val.obj.list_indexes, list)
        self.assertIsInstance(val.obj.list_indexes[0], ListIndex)
        self.assertEqual(len(val.obj.list_indexes), 1)
        self.assertEqual(val.obj.list_indexes[0].list_index.value, 1)
        self.assertIsInstance(val.dot_access[0], FunCall)
        self.assertEqual(val.dot_access[0].identifier, 'method')
        self.assertEqual(len(val.dot_access[0].arguments), 0)

    def test_parse_simple_assignment(self):
        tokens = [
            Token(TokenType.VAR, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'a'),
            Token(TokenType.ASSIGN_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_variable_declaration()

        self.assertIsInstance(val, VariableAssignment)
        self.assertIsInstance(val.variable, Identifier)
        self.assertIsInstance(val.value, Term)
        self.assertEqual(val.variable.identifier, 'a')
        self.assertEqual(val.value.value, 1)

    def test_parse_unary_term(self):
        tokens = [
            Token(TokenType.NEGATION_OPERATOR, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'a'),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, NotExpressionLogical)
        self.assertEqual(val.term, Identifier([1, 0], 'a'))

    def test_parse_minus_term(self):
        tokens = [
            Token(TokenType.SUBTRACT_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, NotExpressionAritmetic)
        self.assertEqual(val.term, Term([1, 0], TermType.INT, 1))

    def test_parse_power_expression(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.POWER_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, PowerExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 3))

    def test_parse_multiplication_expression(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, MultiplicationExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 3))

        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, MultiplicationExpression)
        self.assertIsInstance(val.left, MultiplicationExpression)
        self.assertEqual(val.left.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.left.right, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 4))

    def test_parse_division_expression(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, DivisionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 3))

    def test_parse_division_with_multiplication(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, DivisionExpression)
        self.assertIsInstance(val.left, MultiplicationExpression)
        self.assertEqual(val.left.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.left.right, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 4))

    def test_parse_division_expression_with_power(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.POWER_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, DivisionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertIsInstance(val.right, PowerExpression)
        self.assertEqual(val.right.left, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right.right, Term([1, 0], TermType.INT, 2))

    def test_parse_addition_expression(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.ADD_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, AdditionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 3))

    def test_parse_addition_with_multiplication(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.ADD_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, AdditionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertIsInstance(val.right, MultiplicationExpression)
        self.assertEqual(val.right.left, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right.right, Term([1, 0], TermType.INT, 4))

        tokens = [
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.ADD_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, MultiplicationExpression)
        self.assertIsInstance(val.left, AdditionExpression)
        self.assertEqual(val.left.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.left.right, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 4))

    def test_parse_subtraction_expression(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.SUBTRACT_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, SubtractionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.right, Term([1, 0], TermType.INT, 3))

    def test_parse_subtraction_with_division(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.SUBTRACT_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, SubtractionExpression)
        self.assertEqual(val.left, Term([1, 0], TermType.INT, 2))
        self.assertIsInstance(val.right, DivisionExpression)
        self.assertEqual(val.right.left, Term([1, 0], TermType.INT, 3))
        self.assertEqual(val.right.right, Term([1, 0], TermType.INT, 4))

        tokens = [
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.SUBTRACT_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 4),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)

        val = parser.parse_expression()

        self.assertIsInstance(val, DivisionExpression)
        self.assertIsInstance(val.left, SubtractionExpression)
        self.assertEqual(val.left.left, Term([1, 0], TermType.INT, 2))
        self.assertEqual(val.left.right, Term([1, 0], TermType.INT, 3))

    def test_parse_invalid_syntax(self):
        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.MULTIPLY_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.DIVIDE_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.LESS_THAN_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.MORE_THAN_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.LESS_OR_EQUAL_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.MORE_OR_EQUAL_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.NOT_EQUAL_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.EQUAL_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.AND_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.OR_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.ADD_OPERATOR, POS, None),
            Token(TokenType.ADD_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'object'),
            Token(TokenType.POINT, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_object()

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'i'),
            Token(TokenType.ASSIGN_OPERATOR, POS, None),
            Token(TokenType.END_OF_FILE, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_assignment_or_object()

    def test_unexpected_token(self):
        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'i'),
            Token(TokenType.ASSIGN_OPERATOR, POS, None),
            Token(TokenType.INTEGER, POS, 5),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'i'),
            Token(TokenType.ASSIGN_OPERATOR, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'fun'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'i'),
            Token(TokenType.ASSIGN_OPERATOR, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'fun'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        tokens = [
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_operation_block()

        tokens = [
            Token(TokenType.DEF, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'func'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.RETURN, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_function_definition()

        tokens = [
            Token(TokenType.BREAK, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_break_statement()

        tokens = [
            Token(TokenType.IF, POS, None),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'cond'),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'do'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.SEMICOLON, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_if_statement()

        tokens = [
            Token(TokenType.IF, POS, None),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'cond'),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.RIGHT_CURLY_BRACKETS, POS, None),
            Token(TokenType.ELSE, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_if_statement()

        tokens = [
            Token(TokenType.LEFT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.COMMA, POS, None),
            Token(TokenType.INTEGER, POS, 2),
            Token(TokenType.COMMA, POS, None),
            Token(TokenType.INTEGER, POS, 3),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_list()

        tokens = [
            Token(TokenType.DEF, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'func'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'a'),
            Token(TokenType.COMMA, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'b'),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.DEF, POS, None),
            Token(TokenType.IDENTIFIER, POS, 'func2'),
            Token(TokenType.LEFT_PARENTHASIS, POS, None),
            Token(TokenType.RIGHT_PARENTHASIS, POS, None),
            Token(TokenType.LEFT_CURLY_BRACKETS, POS, None),
            Token(TokenType.RIGHT_CURLY_BRACKETS, POS, None),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_function_definition()

        tokens = [
            Token(TokenType.IDENTIFIER, POS, 'i'),
            Token(TokenType.LEFT_SQUARE_BRACKETS, POS, None),
            Token(TokenType.INTEGER, POS, 1),
            Token(TokenType.END_OF_FILE, POS, None)
        ]
        lexer = MockLexer(tokens)
        parser = Parser(lexer)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_object()
