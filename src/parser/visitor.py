from src.parser.parser_tree import (
    Program,
    OperationBlock,
    BreakStatement,
    ReturnStatement,
    Assignment,
    Call,
    SingleCall,
    Parameter,
    FunctionDefinition,
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
    List,
    ListIndex,
    Term
)


class Visitor:
    def __init__(self):
        pass

    def visit(self, node):
        return node.accept_visitor(self)

    def do_for_program(self, node: Program):
        pass

    def do_for_operation_block(self, node: OperationBlock):
        pass

    def do_for_break_statement(self, node: BreakStatement):
        pass

    def do_for_return_statement(self, node: ReturnStatement):
        pass

    def do_for_assignment(self, node: Assignment):
        pass

    def do_for_call(self, node: Call):
        pass

    def do_for_single_call(self, node: SingleCall):
        pass

    def do_for_function_definition(self, node: FunctionDefinition):
        pass

    def do_for_parameter(self, node: Parameter):
        pass

    def do_for_list_index(self, node: ListIndex):
        pass

    def do_for_if_statement(self, node: IfStatement):
        pass

    def do_for_while_statement(self, node: WhileStatement):
        pass

    def do_for_for_statement(self, node: ForStatement):
        pass

    def do_for_or_expr(self, node: OrExpression):
        pass

    def do_for_and_expr(self, node: AndExpression):
        pass

    def do_for_less_than_expr(self, node: LessThanExpression):
        pass

    def do_for_greater_than_expr(self, node: GreaterThanExpression):
        pass

    def do_for_less_or_equal_expr(self, node: LessOrEqualExpression):
        pass

    def do_for_greater_or_equal_expr(self, node: GreaterOrEqualExpression):
        pass

    def do_for_equality_expr(self, node: EqualityExpression):
        pass

    def do_for_inequality_expr(self, node: InequalityExpression):
        pass

    def do_for_addition_expr(self, node: AdditionExpression):
        pass

    def do_for_subtraction_expr(self, node: SubtractionExpression):
        pass

    def do_for_multiplication_expr(self, node: MultiplicationExpression):
        pass

    def do_for_division_expr(self, node: DivisionExpression):
        pass

    def do_for_power_expr(self, node: PowerExpression):
        pass

    def do_for_not_expr(self, node: NotExpression):
        pass

    def do_for_term(self, node: Term):
        pass

    def do_for_list(self, node: List):
        pass
