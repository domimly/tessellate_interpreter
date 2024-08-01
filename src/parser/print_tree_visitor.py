from src.parser.visitor import Visitor
from src.parser.parser_tree import (
    Node,
    Program,
    OperationBlock,
    BreakStatement,
    ReturnStatement,
    Assignment,
    Call,
    SingleCall,
    FunctionDefinition,
    Parameter,
    IfStatement,
    WhileStatement,
    ForStatement,
    OrExpression,
    AndExpression,
    LessThanExpression,
    GreaterThanExpression,
    LessOrEqualExpression,
    GreaterOrEqualExpression,
    EqualityExpression,
    InequalityExpression,
    AdditionExpression,
    SubtractionExpression,
    MultiplicationExpression,
    DivisionExpression,
    PowerExpression,
    NotExpression,
    Term,
    List,
    ListIndex
)


class PrintTreeVisitor(Visitor):
    def __init__(self):
        self.indent = 0

    def visit(self, node: Node):
        if node:
            self.indent += 1
            super().visit(node)
            self.indent -= 1

    def print(self, operation, position, value=None, node_type=None):
        msg = ' ' * self.indent * 4 + f'{operation} at {position}'
        print(msg)

    def print_extra_info(self, info):
        print(' ' * self.indent * 4 + info)

    def do_for_program(self, node: Program):
        self.print('Program', node.position)
        for statement in node.statements:
            self.visit(statement)

    def do_for_operation_block(self, node: OperationBlock):
        self.print('Operation Block', node.position)
        for statement in node.statements:
            self.visit(statement)

    def do_for_break_statement(self, node: BreakStatement):
        self.print('Break Statement', node.position)

    def do_for_return_statement(self, node: ReturnStatement):
        self.print('Return Statement', node.position)
        self.print_extra_info('^value:')
        self.visit(node.value)

    def do_for_assignment(self, node: Assignment):
        self.print('Assignment', node.position)
        self.print_extra_info('^assigned to:')
        self.visit(node.call)
        self.print_extra_info('^expression assigned:')
        self.visit(node.value)

    def do_for_call(self, node: Call):
        self.print('Call', node.position)
        for single_call in node.call:
            self.visit(single_call)

    def do_for_single_call(self, node: SingleCall):
        self.print('Single Call', node.position)
        self.print_extra_info(f'^name: {node.identifier}')
        if node.list_index:
            self.print_extra_info(f'^list_index: {node.list_index}')
        self.print_extra_info(f'^number of args: {len(node.arguments)}')
        for argument in node.arguments:
            self.visit(argument)

    def do_for_function_definition(self, node: FunctionDefinition):
        self.print('Function Definition', node.position)
        self.print_extra_info(f'^name: {node.identifier}')
        self.print_extra_info(f'^number of parameters: {len(node.parameters)}')
        for parameter in node.parameters:
            self.visit(parameter)
        self.visit(node.operation_block)

    def do_for_parameter(self, node: Parameter):
        self.print('Parameter', node.position)
        self.print_extra_info(f'name: {node.identifier}')

    def do_for_if_statement(self, node: IfStatement):
        self.print('If Statement', node.position)
        self.print_extra_info('^condition:')
        self.visit(node.condition)
        self.print_extra_info('^if operation:')
        self.visit(node.if_operation)
        if node.else_operation:
            self.print_extra_info('^else operation:')
            self.visit(node.else_operation)

    def do_for_while_statement(self, node: WhileStatement):
        self.print('While Statement', node.position)
        self.print_extra_info('^condition:')
        self.visit(node.condition)
        self.print_extra_info('^operation:')
        self.visit(node.operation)

    def do_for_for_statement(self, node: ForStatement):
        self.print('For Statement', node.position)
        self.print_extra_info(f'^iterable: {node.iterable}')
        self.print_extra_info('^iterable list:')
        self.visit(node.iterable_list)
        self.print_extra_info('^operation:')
        self.visit(node.operation)

    def do_for_or_expr(self, node: OrExpression):
        self.print('Or Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_and_expr(self, node: AndExpression):
        self.print('And Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_less_than_expr(self, node: LessThanExpression):
        self.print('Less Than Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_greater_than_expr(self, node: GreaterThanExpression):
        self.print('Greater Than Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_less_or_equal_expr(self, node: LessOrEqualExpression):
        self.print('Less Or Equal Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_greater_or_equal_expr(self, node: GreaterOrEqualExpression):
        self.print('Greater Or Equal Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_equality_expr(self, node: EqualityExpression):
        self.print('Equality Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_inequality_expr(self, node: InequalityExpression):
        self.print('Inequality Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_addition_expr(self, node: AdditionExpression):
        self.print('Addition Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_subtraction_expr(self, node: SubtractionExpression):
        self.print('Subtraction Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_multiplication_expr(self, node: MultiplicationExpression):
        self.print('Multiplication Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_division_expr(self, node: DivisionExpression):
        self.print('Division Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_power_expr(self, node: PowerExpression):
        self.print('Power Expression', node.position)
        self.visit(node.left)
        self.visit(node.right)

    def do_for_not_expr(self, node: NotExpression):
        self.print('Not Expression', node.position)
        self.visit(node.term)

    def do_for_term(self, node: Term):
        self.print('Term', node.position)
        self.print_extra_info(f'^value: {node.value}')
        self.print_extra_info(f'^type: {node.term_type}')

    def do_for_list(self, node: List):
        self.print('List', node.position)
        for element in node.contents:
            self.visit(element)

    def do_for_list_index(self, node: ListIndex):
        self.print('List Index', node.position)
        self.print_extra_info(f'^index: {node.index}')
