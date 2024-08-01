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
    SingleCall,
    Call,
    Assignment,
    NotExpression,
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

    def test_parse_single_call(self):
        text = 'identifier'
        parser = self.init_parser(text)
        val = parser.parse_single_call()
        assert isinstance(val, SingleCall)
        assert val.identifier == 'identifier'
        assert val.arguments == []

    def test_parse_call_with_params(self):
        text = 'func(a, b)'
        parser = self.init_parser(text)
        val = parser.parse_single_call()
        assert isinstance(val, SingleCall)
        assert val.identifier == 'func'
        assert len(val.arguments) == 2

    def test_parse_call_with_list_index(self):
        text = 'object[1]'
        parser = self.init_parser(text)
        val = parser.parse_single_call()
        assert isinstance(val, SingleCall)
        assert val.identifier == 'object'
        assert len(val.arguments) == 0
        assert val.list_index.index == 1

    def test_parse_call(self):
        text = 'object.attribute.method()'
        parser = self.init_parser(text)
        val = parser.parse_call()
        assert isinstance(val, Call)
        assert len(val.call) == 3
        assert isinstance(val.call[0], SingleCall)
        assert val.call[0].identifier == 'object'
        assert len(val.call[0].arguments) == 0
        assert isinstance(val.call[1], SingleCall)
        assert val.call[1].identifier == 'attribute'
        assert len(val.call[1].arguments) == 0
        assert isinstance(val.call[2], SingleCall)
        assert val.call[2].identifier == 'method'
        assert len(val.call[2].arguments) == 0

        text = 'object[1].method()'
        parser = self.init_parser(text)
        val = parser.parse_call()
        assert isinstance(val, Call)
        assert len(val.call) == 2
        assert isinstance(val.call[0], SingleCall)
        assert val.call[0].identifier == 'object'
        assert len(val.call[0].arguments) == 0
        assert isinstance(val.call[0].list_index, ListIndex)
        assert val.call[0].list_index.index == 1
        assert isinstance(val.call[1], SingleCall)
        assert val.call[1].identifier == 'method'
        assert len(val.call[1].arguments) == 0

    def test_parse_simple_assignment(self):
        text = 'a = 1;'
        parser = self.init_parser(text)
        val = parser.parse_assignment_or_call()
        assert isinstance(val, Assignment)
        assert isinstance(val.call, Call)
        assert isinstance(val.value, Term)
        assert val.call.call[0].identifier == 'a'
        assert val.value.value == 1

    def test_parse_unary_term(self):
        text = '!a'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, NotExpression)
        assert val.term == Call([1, 2], [SingleCall([1, 2], 'a', [])])

    def test_parse_minus_term(self):
        text = '-1'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, NotExpression)
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
        assert isinstance(val.left, Call)
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
        assert val.left == Call([1, 1], [SingleCall([1, 1], 'a', [])])
        assert val.right == Call([1, 7], [SingleCall([1, 7], 'b', [])])

        text = 'a and b and True'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, AndExpression)
        assert val.left == AndExpression(
            [1, 3],
            Call([1, 1], [SingleCall([1, 1], 'a', [])]),
            Call([1, 7], [SingleCall([1, 7], 'b', [])])
        )
        assert val.right == Term([1, 13], TermType.BOOL, True)

    def test_parse_or_expression(self):
        text = 'a or b'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, OrExpression)
        assert val.left == Call([1, 1], [SingleCall([1, 1], 'a', [])])
        assert val.right == Call([1, 6], [SingleCall([1, 6], 'b', [])])

        text = 'a or b or True'
        parser = self.init_parser(text)
        val = parser.parse_expression()
        assert isinstance(val, OrExpression)
        assert val.left == OrExpression(
            [1, 3],
            Call([1, 1], [SingleCall([1, 1], 'a', [])]),
            Call([1, 6], [SingleCall([1, 6], 'b', [])])
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
        assert val.right == Call([1, 24], [SingleCall([1, 24], 'b', [])])
        val = val.left
        assert isinstance(val.left, AdditionExpression)
        assert val.right == Call([1, 19], [SingleCall([1, 19], 'a', [])])
        val = val.left
        assert isinstance(val.left, DivisionExpression)
        assert val.left.left == Term([1, 1], TermType.INT, 1)
        assert val.left.right == Term([1, 5], TermType.INT, 2)
        assert isinstance(val.right, MultiplicationExpression)
        assert val.right.left == Term([1, 9], TermType.INT, 3)
        assert val.right.right == Term([1, 13], TermType.INT, 4)

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
        assert len(val.operation_block.statements) == 1

    def test_for_statement(self):
        text = 'for (i in range(10)){}'
        parser = self.init_parser(text)
        val = parser.parse_for_statement()
        assert isinstance(val, ForStatement)
        assert val.iterable == 'i'
        assert isinstance(val.iterable_list, Call)
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
            parser.parse_call()

        text = 'i =;'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_assignment_or_call()

        text = '[1, 2, 3,'
        parser = self.init_parser(text)
        with pytest.raises(InvalidSyntaxError):
            parser.parse_list()

    def test_unexpected_token(self):
        text = 'i = 5'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_call()

        text = 'i = fun({}'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_call()

        text = 'i = fun('
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_assignment_or_call()

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

        text = 'i[];'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_call()

        text = 'i[1;'
        parser = self.init_parser(text)
        with pytest.raises(UnexpectedTokenError):
            parser.parse_call()
