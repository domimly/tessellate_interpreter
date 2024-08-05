import io
import pytest

from src.lexer.stream import Stream
from src.lexer.lexer import Lexer
from src.constants import (
    MAXIMUM_IDENTIFIER,
    MAXIMUM_STRING,
    MAXIMUM_INT_DIGITS,
    MAXIMUM_FLOAT_DECIMALS
)
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
    Assignment,
    NotExpressionLogical,
    NotExpressionAritmetic,
    PowerExpression,
    MultiplicationExpression,
    DivisionExpression,
    AdditionExpression,
    SubtractionExpression,
    LessThanExpression,
    GreaterThanExpression,
    LessOrEqualExpression,
    GreaterOrEqualExpression,
    InequalityExpression,
    EqualityExpression,
    AndExpression,
    OrExpression,
    OperationBlock,
    Parameter,
    FunctionDefinition,
    ForStatement,
    VariableAssignment,
    WhileStatement,
    IfStatement,
    List,
    ListIndex,
    ReturnStatement,
    BreakStatement
)


class TestParser:
    def init_parser(self, text):
        lexer = Lexer(
            Stream(io.StringIO(text)),
            MAXIMUM_IDENTIFIER,
            MAXIMUM_STRING,
            MAXIMUM_INT_DIGITS,
            MAXIMUM_FLOAT_DECIMALS
        )
        parser = Parser(lexer)
        return parser

    def test_parse_program(self):
        text = 'def func(){return 1;}'
        parser = self.init_parser(text)
        program = parser.parse_program()
        assert len(program.statements) == 1

    def test_parse_int(self):
        text = '420'
        parser = self.init_parser(text)
        val = parser.parse_term()
        assert isinstance(val, Term)
        assert val.value == 420
        assert val.term_type == TermType.INT

    def test_parse_float(self):
        text = '3.14'
        parser = self.init_parser(text)
        val = parser.parse_term()
        assert isinstance(val, Term)
        assert val.value == 3.14
        assert val.term_type == TermType.FLOAT

    def test_parse_string(self):
        text = '"hello"'
        parser = self.init_parser(text)
        val = parser.parse_term()
        assert isinstance(val, Term)
        assert val.value == 'hello'
        assert val.term_type == TermType.STRING

    def test_parse_bool_true(self):
        text = 'True'
        parser = self.init_parser(text)
        val = parser.parse_term()
        assert isinstance(val, Term)
        assert val.value in [True]
        assert val.term_type == TermType.BOOL

    def test_parse_bool_false(self):
        text = 'False'
        parser = self.init_parser(text)
        val = parser.parse_term()
        assert isinstance(val, Term)
        assert val.value in [False]
        assert val.term_type == TermType.BOOL

    def test_parse_single_object(self):
        text = 'identifier'
        parser = self.init_parser(text)
        val = parser.parse_single_object()
        assert isinstance(val, Identifier)
        assert val.identifier == 'identifier'

    def test_parse_object_with_params(self):
        text = 'func(a, b)'
        parser = self.init_parser(text)
        val = parser.parse_single_object()
        assert isinstance(val, FunCall)
        assert val.identifier == 'func'
        assert len(val.arguments) == 2

    def test_parse_object_with_list_index(self):
        text = 'object[1]'
        parser = self.init_parser(text)
        val = parser.parse_single_object()
        assert isinstance(val, ListIndexAccess)
        assert val.identifier == 'object'
        assert len(val.list_indexes) == 1
        assert val.list_indexes[0].list_index.value == 1

    def test_parse_object(self):
        text = 'object.attribute.method()'
        parser = self.init_parser(text)
        val = parser.parse_object()
        assert isinstance(val, DotAccess)
        assert isinstance(val.obj, Identifier)
        assert len(val.dot_access) == 2
        assert val.obj.identifier == 'object'
        assert isinstance(val.dot_access[0], Identifier)
        assert val.dot_access[0].identifier == 'attribute'
        assert isinstance(val.dot_access[1], FunCall)
        assert val.dot_access[1].identifier == 'method'
        assert len(val.dot_access[1].arguments) == 0

        text = 'object[1].method()'
        parser = self.init_parser(text)
        val = parser.parse_object()
        assert isinstance(val, DotAccess)
        assert len(val.dot_access) == 1
        assert isinstance(val.obj, ListIndexAccess)
        assert val.obj.identifier == 'object'
        assert isinstance(val.obj.list_indexes, list)
        assert isinstance(val.obj.list_indexes[0], ListIndex)
        assert len(val.obj.list_indexes) == 1
        assert val.obj.list_indexes[0].list_index.value == 1
        assert isinstance(val.dot_access[0], FunCall)
        assert val.dot_access[0].identifier == 'method'
        assert len(val.dot_access[0].arguments) == 0

    def test_parse_simple_assignment(self):
        text = 'var a = 1;'
        parser = self.init_parser(text)
        val = parser.parse_variable_declaration()
        assert isinstance(val, VariableAssignment)
        assert isinstance(val.variable, Identifier)
        assert isinstance(val.value, Term)
        assert val.variable.identifier == 'a'
        assert val.value.value == 1

    def test_parse_unary_term(self):
        text = '!a'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, NotExpressionLogical)
        assert val.term == Identifier([1, 2], 'a')

    def test_parse_minus_term(self):
        text = '-1'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, NotExpressionAritmetic)
        assert val.term == Term([1, 2], TermType.INT, 1)

    def test_parse_power_expression(self):
        text = '2 ** 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, PowerExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_parse_multiplication_expression(self):
        text = '2 * 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, MultiplicationExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

        text = '2 * 3 * 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, MultiplicationExpression)
        assert val.left == MultiplicationExpression(
            [1, 3],
            Term([1, 1], TermType.INT, 2),
            Term([1, 5], TermType.INT, 3)
        )
        assert val.right == Term([1, 9], TermType.INT, 4)

    def test_parse_division_expression(self):
        text = '2 / 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, DivisionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

    def test_parse_division_with_multiplication(self):
        text = '2 * 3 / 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, DivisionExpression)
        assert val.left == MultiplicationExpression(
            [1, 3],
            Term([1, 1], TermType.INT, 2),
            Term([1, 5], TermType.INT, 3)
        )
        assert val.right == Term([1, 9], TermType.INT, 4)

    def test_parse_division_expression_with_power(self):
        text = '2 / 3**2'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, DivisionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == PowerExpression(
            [1, 6],
            Term([1, 5], TermType.INT, 3),
            Term([1, 8], TermType.INT, 2)
        )

    def test_parse_addition_expression(self):
        text = '2 + 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AdditionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

    def test_parse_addition_with_multiplication(self):
        text = '2 + 3 * 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AdditionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == MultiplicationExpression(
            [1, 7],
            Term([1, 5], TermType.INT, 3),
            Term([1, 9], TermType.INT, 4)
        )

        text = '(2 + 3) * 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, MultiplicationExpression)
        assert val.left == AdditionExpression(
            [1, 4],
            Term([1, 2], TermType.INT, 2),
            Term([1, 6], TermType.INT, 3)
        )
        assert val.right == Term([1, 11], TermType.INT, 4)

    def test_parse_subtraction_expression(self):
        text = '2 - 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, SubtractionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

    def test_parse_subtraction_with_division(self):
        text = '2 - 3 / 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, SubtractionExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == DivisionExpression(
            [1, 7],
            Term([1, 5], TermType.INT, 3),
            Term([1, 9], TermType.INT, 4)
        )

        text = '(2 - 3) / 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, DivisionExpression)
        assert val.left == SubtractionExpression(
            [1, 4],
            Term([1, 2], TermType.INT, 2),
            Term([1, 6], TermType.INT, 3)
        )
        assert val.right == Term([1, 11], TermType.INT, 4)

    def test_parse_less_than_expression(self):
        text = '2 < 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, LessThanExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

        text = 'a.b() < 4'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, LessThanExpression)
        assert isinstance(val.left, DotAccess)
        assert val.right == Term([1, 9], TermType.INT, 4)

    def test_parse_greater_than_expression(self):
        text = '2 > 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, GreaterThanExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 5], TermType.INT, 3)

    def test_parse_less_or_equal_expression(self):
        text = '2 <= 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, LessOrEqualExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_parse_greater_or_equal_expression(self):
        text = '2 >= 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, GreaterOrEqualExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_parse_inequality_expression(self):
        text = '2 != 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, InequalityExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_parse_equality_expression(self):
        text = '2 == 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, EqualityExpression)
        assert val.left == Term([1, 1], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_parse_and_expression(self):
        text = 'a and b'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AndExpression)
        assert val.left == Identifier([1, 1], 'a')
        assert val.right == Identifier([1, 7], 'b')

        text = 'a and b and True'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AndExpression)
        assert val.left == AndExpression(
            [1, 3],
            Identifier([1, 1], 'a'),
            Identifier([1, 7], 'b')
        )
        assert val.right == Term([1, 13], TermType.BOOL, True)

    def test_parse_or_expression(self):
        text = 'a or b'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, OrExpression)
        assert val.left == Identifier([1, 1], 'a')
        assert val.right == Identifier([1, 6], 'b')

        text = 'a or b or True'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, OrExpression)
        assert val.left == OrExpression(
            [1, 3],
            Identifier([1, 1], 'a'),
            Identifier([1, 6], 'b')
        )
        assert val.right == Term([1, 11], TermType.BOOL, True)

    def test_parse_expression_with_parenthesis(self):
        text = '(2 + 3)'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AdditionExpression)
        assert val.left == Term([1, 2], TermType.INT, 2)
        assert val.right == Term([1, 6], TermType.INT, 3)

    def test_operations_priority(self):
        text = '1 / 2 + 3 * 4 and a or b'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, OrExpression)
        assert isinstance(val.left, AndExpression)
        assert val.right == Identifier([1, 24], 'b')
        val = val.left
        assert isinstance(val.left, AdditionExpression)
        assert val.right == Identifier([1, 19], 'a')
        val = val.left
        assert isinstance(val.left, DivisionExpression)
        assert val.left.left == Term([1, 1], TermType.INT, 1)
        assert val.left.right == Term([1, 5], TermType.INT, 2)
        assert isinstance(val.right, MultiplicationExpression)
        assert val.right.left == Term([1, 9], TermType.INT, 3)
        assert val.right.right == Term([1, 13], TermType.INT, 4)

        text = '(1 + 2) * 3'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, MultiplicationExpression)
        assert isinstance(val.left, AdditionExpression)
        assert val.right == Term([1, 11], TermType.INT, 3)
        val = val.left
        assert val.left == Term([1, 2], TermType.INT, 1)
        assert val.right == Term([1, 6], TermType.INT, 2)

        text = '(a or b) and (c and d)'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AndExpression)
        assert isinstance(val.left, OrExpression)
        assert isinstance(val.right, AndExpression)
        left = val.left
        right = val.right
        assert left.left == Identifier([1, 2], 'a')
        assert left.right == Identifier([1, 7], 'b')
        assert right.left == Identifier([1, 15], 'c')
        assert right.right == Identifier([1, 21], 'd')

    def test_parse_operation_block(self):
        text = '{a = b; return 1;}'
        parser = self.init_parser(text)
        val = parser.parse_operation_block()
        assert isinstance(val, OperationBlock)
        assert len(val.statements) == 2
        assert isinstance(val.statements[0], Assignment)
        assert isinstance(val.statements[1], ReturnStatement)

    def test_function_definition(self):
        text = 'def func(a, b){return 1;}'
        parser = self.init_parser(text)
        val = parser.parse_function_definition()
        assert isinstance(val, FunctionDefinition)
        assert val.identifier == 'func'
        assert len(val.parameters) == 2
        assert isinstance(val.parameters[0], Parameter)
        assert isinstance(val.parameters[1], Parameter)
        assert len(val.body.statements) == 1

    def test_for_statement(self):
        text = 'for (i in range(10)){}'
        parser = self.init_parser(text)
        val = parser.parse_for_statement()
        assert isinstance(val, ForStatement)
        assert val.iterable == 'i'
        assert isinstance(val.iterable_list, FunCall)
        assert len(val.operation.statements) == 0

    def test_while_statement(self):
        text = 'while (True){}'
        parser = self.init_parser(text)
        val = parser.parse_while_statement()
        assert isinstance(val, WhileStatement)
        assert isinstance(val.condition, Term)
        assert len(val.operation.statements) == 0

    def test_if_statement(self):
        text = 'if (True){}'
        parser = self.init_parser(text)
        val = parser.parse_if_statement()
        assert isinstance(val, IfStatement)
        assert isinstance(val.condition, Term)
        assert len(val.if_operation.statements) == 0

    def test_if_else_statement(self):
        text = 'if (True){} else {}'
        parser = self.init_parser(text)
        val = parser.parse_if_statement()
        assert isinstance(val, IfStatement)
        assert isinstance(val.condition, Term)
        assert len(val.if_operation.statements) == 0
        assert len(val.else_operation.statements) == 0

    def test_list(self):
        text = '[1, 2, 3]'
        parser = self.init_parser(text)
        val = parser.parse_list()
        assert isinstance(val, List)
        assert len(val.contents) == 3
        assert val.contents[0].value == 1
        assert val.contents[1].value == 2
        assert val.contents[2].value == 3

    def test_return_statement(self):
        text = 'return 1;'
        parser = self.init_parser(text)
        val = parser.parse_return_statement()
        assert isinstance(val, ReturnStatement)
        assert val.value.value == 1

    def test_break_statement(self):
        text = 'break;'
        parser = self.init_parser(text)
        val = parser.parse_break_statement()
        assert isinstance(val, BreakStatement)

    def test_invalid_syntax(self):
        text = '1 +'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 -'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 *'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 /'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 <'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 >'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 <='
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 >='
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 !='
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 =='
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 and'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 or'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = '1 + 2 +'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_expression()

        text = 'object.'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_object()

        text = 'i =;'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_assignment_or_object()

        text = '[1, 2, 3,'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_list()

    def test_unexpected_token(self):
        text = 'i = 5'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        text = 'i = fun({}'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        text = 'i = fun('
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_object()

        text = '{'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_operation_block()

        text = 'def func(){return 1;'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_function_definition()

        text = 'break'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_break_statement()

        text = 'if (cond) do();'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_if_statement()

        text = 'if (cond){} else'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_if_statement()

        text = '[1, 2, 3'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_list()

        text = 'def func(a, b){def func2(){}}'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_function_definition()

        text = 'i[1;'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_object()
