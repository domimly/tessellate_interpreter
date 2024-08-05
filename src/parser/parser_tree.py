from enum import Enum, auto
from dataclasses import dataclass


class TermType(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    LIST = auto()


@dataclass
class Node:
    position: list

    def accept_visitor(self, visitor):
        pass


@dataclass
class Statement(Node):
    pass


@dataclass
class Expression(Node):
    pass


@dataclass
class Identifier(Node):
    identifier: str

    def accept_visitor(self, visitor):
        visitor.do_for_identifier(self)


@dataclass
class Variable(Node):
    identifier: str

    def accept_visitor(self, visitor):
        visitor.do_for_variable(self)


@dataclass
class OperationBlock(Node):
    statements: list[Statement]

    def accept_visitor(self, visitor):
        visitor.do_for_operation_block(self)


@dataclass
class OrExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_or_expr(self)


@dataclass
class AndExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_and_expr(self)


@dataclass
class MultiplicationExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_multiplication_expr(self)


@dataclass
class DivisionExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_division_expr(self)


@dataclass
class AdditionExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_addition_expr(self)


@dataclass
class SubtractionExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_subtraction_expr(self)


@dataclass
class LessThanExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_less_than_expr(self)


@dataclass
class GreaterThanExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_greater_than_expr(self)


@dataclass
class LessOrEqualExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_less_or_equal_expr(self)


@dataclass
class GreaterOrEqualExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_greater_or_equal_expr(self)


@dataclass
class EqualityExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_equality_expr(self)


@dataclass
class InequalityExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_inequality_expr(self)


@dataclass
class PowerExpression(Expression):
    left: Expression
    right: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_power_expr(self)


@dataclass
class NotExpressionLogical(Expression):
    term: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_not_expr_logical(self)


@dataclass
class NotExpressionAritmetic(Expression):
    term: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_not_expr_aritmetic(self)


@dataclass
class Term(Expression):
    term_type: TermType
    value: int | float | bool | str | list

    def accept_visitor(self, visitor):
        visitor.do_for_term(self)


@dataclass
class Parameter(Node):
    identifier: str

    def accept_visitor(self, visitor):
        visitor.do_for_parameter(self)


@dataclass
class ListIndex(Node):
    list_index: int | Expression

    def accept_visitor(self, visitor):
        visitor.do_for_list_index(self)


@dataclass
class ListIndexAccess(Node):
    identifier: str
    list_indexes: list[ListIndex]

    def accept_visitor(self, visitor):
        visitor.do_for_list_index_access(self)


@dataclass
class FunCall(Node):
    identifier: str
    arguments: list[Expression]

    def accept_visitor(self, visitor):
        visitor.do_for_fun_call(self)


@dataclass
class DotAccess(Node):
    obj: Identifier | FunCall | ListIndexAccess
    dot_access: list[Identifier | FunCall]

    def accept_visitor(self, visitor):
        visitor.do_for_dot_access(self)


@dataclass
class List(Expression):
    contents: list[Expression]

    def accept_visitor(self, visitor):
        visitor.do_for_list(self)


@dataclass
class Tuple(Node):
    contents: tuple[Expression]

    def accept_visitor(self, visitor):
        visitor.do_for_tuple(self)


@dataclass
class Program(Node):
    statements: list[Statement]

    def accept_visitor(self, visitor):
        visitor.do_for_program(self)


@dataclass
class Assignment(Statement):
    object: ListIndexAccess | FunCall | DotAccess
    value: Expression | List

    def accept_visitor(self, visitor):
        visitor.do_for_assignment(self)


@dataclass
class VariableAssignment(Statement):
    variable: Identifier
    value: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_variable_assignment(self)


@dataclass
class BreakStatement(Statement):
    pass

    def accept_visitor(self, visitor):
        visitor.do_for_break_statement(self)


@dataclass
class ReturnStatement(Statement):
    value: Expression

    def accept_visitor(self, visitor):
        visitor.do_for_return_statement(self)


@dataclass
class IfStatement(Statement):
    condition: Expression
    if_operation: Statement
    else_operation: Statement = None

    def accept_visitor(self, visitor):
        visitor.do_for_if_statement(self)


@dataclass
class WhileStatement(Statement):
    condition: Expression
    operation: list[Statement]

    def accept_visitor(self, visitor):
        visitor.do_for_while_statement(self)


@dataclass
class ForStatement(Statement):
    iterable: Identifier
    iterable_list: List
    operation: list[Statement]

    def accept_visitor(self, visitor):
        visitor.do_for_for_statement(self)


@dataclass
class FunctionDefinition(Statement):
    identifier: str
    parameters: list[Parameter]
    body: OperationBlock

    def accept_visitor(self, visitor):
        visitor.do_for_function_definition(self)


@dataclass
class AttributeAccess(Node):
    object: Identifier | FunCall | ListIndexAccess
    attribute: Identifier

    def accept_visitor(self, visitor):
        visitor.do_for_attribute_access(self)


@dataclass
class MethodCall(Node):
    object: Identifier | FunCall | ListIndexAccess
    method: FunCall

    def accept_visitor(self, visitor):
        visitor.do_for_method_call(self)
