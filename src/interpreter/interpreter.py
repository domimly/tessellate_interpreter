from src.error_handling.interpreter_error import (
    BaseForInvalidNumberOfArgumentsError,
    BreakOutsideLoopError,
    DivisionByZeroError,
    FunctionRedefinitionError,
    IndexOutOfRangeError,
    InvalidConstructorArgumentsError,
    InvalidFunCallArgumentsError,
    InvalidIndexError,
    InvalidNumberOfArgumentsError,
    InvalidTypeError,
    InvalidVariableAssignmentError,
    IterableNameError,
    MismatchedTypesError,
    NonExistingAttributeError,
    NonExistingFunctionError,
    NonExistingMethodError,
    NonExistingVariableError,
    RecursionLimitError,
    ReturnOutsideFunctionError,
    TypeCastingError,
    VariableRedeclarationError
)

from src.parser.parser_tree import (
    Assignment,
    BreakStatement,
    DotAccess,
    ForStatement,
    FunCall,
    FunctionDefinition,
    Identifier,
    IfStatement,
    List,
    ListIndex,
    ListIndexAccess,
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
    NotExpressionLogical,
    NotExpressionAritmetic,
    Term,
    Program,
    OperationBlock,
    ReturnStatement,
    VariableAssignment,
    WhileStatement,
)
from src.interpreter.context import (
    BaseForInvalidConstructorArgumentsError,
    BaseForInvalidFunCallArgumentsError,
    BaseForTypeCastingError,
    Context,
    EmbeddedFunction,
    GlobalContext,
    Scope,
    UserFunction
)
from src.interpreter.symbol_table import Symbol
from src.parser.visitor import Visitor


class Interpreter(Visitor):
    def __init__(self, max_recursion_depth):
        self.max_recursion_depth = max_recursion_depth
        self.global_scope = Scope()
        self.global_context = GlobalContext(self.global_scope)
        self.context_stack = [self.global_context]
        self.in_funcall = False
        self.current_function = None
        self.recursion_counter = 0
        self.ret = False
        self.last_result = None

    def current_context(self):
        return self.context_stack[-1]

    def current_scope(self):
        return self.current_context().scope_stack[-1]

    def global_context(self):
        return self.global_context

    def do_for_program(self, node: Program):
        for statement in node.statements:
            statement.accept_visitor(self)
            self.last_result = None

    def do_for_function_definition(self, node: FunctionDefinition):
        if self.global_context.get_function(node.identifier):
            raise FunctionRedefinitionError(
                node.position,
                node.identifier
            )
        function = UserFunction(node.parameters, node.body)
        self.global_context.set_function(node.identifier, function)

    def do_for_fun_call(self, node: FunCall):
        new_context = Context(self.global_scope)
        self.context_stack.append(new_context)
        if function := self.global_context.get_function(node.identifier):
            self.in_funcall = True
            if self.current_function == function:
                self.recursion_counter += 1
                if self.recursion_counter > self.max_recursion_depth:
                    raise RecursionLimitError(
                        node.position,
                        node.identifier
                    )
            else:
                self.current_function = function

            self.last_result = node.arguments
            try:
                function.accept_visitor(self)
            except BaseForInvalidNumberOfArgumentsError as e:
                raise InvalidNumberOfArgumentsError(
                    node.position,
                    node.identifier,
                    e.expected,
                    e.got
                )
            except BaseForTypeCastingError as e:
                raise TypeCastingError(
                    node.position,
                    e.type_name,
                    e.got
                )
            except BaseForInvalidConstructorArgumentsError as e:
                raise InvalidConstructorArgumentsError(
                    node.position,
                    e.class_name
                )
            except BaseForInvalidFunCallArgumentsError as e:
                raise InvalidFunCallArgumentsError(
                    node.position,
                    e.fun_name
                )
            self.in_funcall = False
            self.current_function = None
            self.recursion_counter = 0
            self.ret = False
            self.context_stack.pop()

        else:
            raise NonExistingFunctionError(
                node.position,
                node.identifier
            )

    def do_for_embedded_function(self, node: EmbeddedFunction):
        call_arguments = self.last_result
        arguments = []
        for arg in call_arguments:
            arg.accept_visitor(self)
            arguments.append(self.last_result.value)
        if (
            node.number_of_parameters and
            len(arguments) != node.number_of_parameters
        ):
            raise BaseForInvalidNumberOfArgumentsError(
                node.number_of_parameters,
                len(arguments)
            )
        try:
            self.last_result = node.body(arguments)
        except BaseForTypeCastingError as e:
            e.got = type(arguments[0]).__name__
            raise e

    def do_for_user_function(self, node: UserFunction):
        call_arguments = self.last_result
        if len(node.parameters) != len(call_arguments):
            raise BaseForInvalidNumberOfArgumentsError(
                len(node.parameters),
                len(call_arguments)
            )
        for param, arg in zip(node.parameters, call_arguments):
            arg.accept_visitor(self)
            self.current_scope().set(
                param.identifier,
                Symbol(self.last_result.get_value())
            )
        node.body.accept_visitor(self)

    def do_for_operation_block(self, node: OperationBlock):
        new_scope = Scope(self.current_scope())
        self.current_context().scope_stack.append(new_scope)
        for statement in node.statements:
            if self.ret is True:
                break
            statement.accept_visitor(self)
        self.current_context().scope_stack.pop()

    def do_for_return_statement(self, node: ReturnStatement):
        if self.in_funcall is False:
            raise ReturnOutsideFunctionError(node.position)
        if node.value:
            node.value.accept_visitor(self)
        self.ret = True

    def do_for_variable_assignment(self, node: VariableAssignment):
        if node.variable.identifier in self.current_scope().symbols:
            raise VariableRedeclarationError(
                node.position,
                node.variable.identifier
            )
        node.value.accept_visitor(self)
        value = self.last_result
        if not value:
            raise InvalidVariableAssignmentError(
                node.position,
                node.variable.identifier
            )
        self.current_scope().set(node.variable.identifier, Symbol(value.value))
        self.last_result = None

    def do_for_assignment(self, node: Assignment):
        node.object.accept_visitor(self)
        obj = self.last_result
        node.value.accept_visitor(self)
        value = self.last_result
        obj.set_value(value.get_value())
        self.last_result = None

    def do_for_dot_access(self, node: DotAccess):
        node.obj.accept_visitor(self)
        obj = self.last_result
        for attr in node.dot_access:
            if isinstance(attr, Identifier):
                try:
                    obj = obj.get_value().attributes[attr.identifier]
                except KeyError:
                    raise NonExistingAttributeError(
                        attr.position,
                        attr.identifier,
                        node.obj.identifier
                    )
            elif isinstance(attr, ListIndexAccess):
                try:
                    obj = obj.get_value().attributes[attr.identifier]
                    for list_index in attr.list_indexes:
                        list_index.accept_visitor(self)
                        index = self.last_result.value
                        try:
                            obj = obj.get_value()[index]
                        except IndexError:
                            raise IndexOutOfRangeError(
                                attr.position,
                                node.obj.identifier
                            )
                        except TypeError:
                            raise InvalidIndexError(
                                attr.position,
                                node.obj.identifier,
                                type(self.last_result.value).__name__
                            )
                except KeyError:
                    raise NonExistingAttributeError(
                        attr.position,
                        attr.identifier,
                        node.obj.identifier
                    )
            elif isinstance(attr, FunCall):
                try:
                    method = obj.get_value().methods[attr.identifier]
                except KeyError:
                    raise NonExistingMethodError(
                        attr.position,
                        attr.identifier,
                        node.obj.identifier
                    )
                arguments = []
                for arg in attr.arguments:
                    arg.accept_visitor(self)
                    arguments.append(self.last_result.value)
                try:
                    obj = method(arguments)
                except BaseForInvalidNumberOfArgumentsError as e:
                    raise InvalidNumberOfArgumentsError(
                        attr.position,
                        attr.identifier,
                        e.expected,
                        e.got
                    )
                except BaseForInvalidFunCallArgumentsError as e:
                    raise InvalidFunCallArgumentsError(
                        attr.position,
                        e.fun_name
                    )
        self.last_result = obj

    def do_for_identifier(self, node: Identifier):
        if val := self.current_scope().get(node.identifier):
            self.last_result = val
        else:
            raise NonExistingVariableError(
                node.position,
                node.identifier
            )

    def do_for_list(self, node: List):
        contents = []
        for content in node.contents:
            content.accept_visitor(self)
            contents.append(self.last_result)
        self.last_result = Symbol(contents)

    def do_for_list_index(self, node: ListIndex):
        node.list_index.accept_visitor(self)

    def do_for_list_index_access(self, node: ListIndexAccess):
        if obj := self.current_scope().get(node.identifier):
            for list_index in node.list_indexes:
                list_index.accept_visitor(self)
                index = self.last_result.value
                try:
                    obj = obj.get_value()[index]
                except IndexError:
                    raise IndexOutOfRangeError(
                        node.position,
                        node.identifier
                    )
                except TypeError:
                    raise InvalidIndexError(
                        node.position,
                        node.identifier,
                        type(self.last_result.value).__name__
                    )
            self.last_result = obj
        else:
            raise NonExistingVariableError(
                node.position,
                node.identifier
            )

    def do_for_if_statement(self, node: IfStatement):
        node.condition.accept_visitor(self)
        if self.last_result.get_value() is True:
            node.if_operation.accept_visitor(self)
        elif node.else_operation:
            node.else_operation.accept_visitor(self)

    def do_for_while_statement(self, node: WhileStatement):
        self.current_context().while_loop_counter += 1
        node.condition.accept_visitor(self)
        condition = self.last_result
        while condition.get_value():
            node.operation.accept_visitor(self)
            if (
                isinstance(self.last_result, BreakStatement) or
                self.ret is True
            ):
                break
            node.condition.accept_visitor(self)
            condition = self.last_result
        self.current_context().while_loop_counter -= 1

    def do_for_break_statement(self, node: BreakStatement):
        if self.current_context().while_loop_counter > 0:
            self.last_result = node
        else:
            raise BreakOutsideLoopError(node.position)

    def do_for_for_statement(self, node: ForStatement):
        node.iterable_list.accept_visitor(self)
        iterable_list = self.last_result.get_value()
        for item in iterable_list:
            if self.current_scope().get(node.iterable):
                raise IterableNameError(
                    node.position,
                    node.iterable
                )
            self.current_scope().set(node.iterable, item)
            node.operation.accept_visitor(self)
            self.current_scope().remove(node.iterable)

    def do_for_or_expr(self, node: OrExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        if not isinstance(left, bool):
            raise InvalidTypeError(
                node.position,
                'boolean',
                type(left).__name__
            )
        if left:
            self.last_result = Symbol(True)
        else:
            node.right.accept_visitor(self)
            right = self.last_result.get_value()
            if not isinstance(right, bool):
                raise InvalidTypeError(
                    node.position,
                    'boolean',
                    type(right).__name__
                )
            if right:
                self.last_result = Symbol(True)
            else:
                self.last_result = Symbol(False)

    def do_for_and_expr(self, node: AndExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        if not isinstance(left, bool):
            raise InvalidTypeError(
                node.position,
                'boolean',
                type(left).__name__
            )
        if not left:
            self.last_result = Symbol(False)
        else:
            node.right.accept_visitor(self)
            right = self.last_result.get_value()
            if not isinstance(right, bool):
                raise InvalidTypeError(
                    node.position,
                    'boolean',
                    type(right).__name__
                )
            if right:
                self.last_result = Symbol(True)
            else:
                self.last_result = Symbol(False)

    def do_for_less_than_expr(self, node: LessThanExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left < right)

    def do_for_greater_than_expr(self, node: GreaterThanExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left > right)

    def do_for_less_or_equal_expr(self, node: LessOrEqualExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left <= right)

    def do_for_greater_or_equal_expr(self, node: GreaterOrEqualExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left >= right)

    def do_for_equality_expr(self, node: EqualityExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if type(left) is not type(right):
            raise MismatchedTypesError(node.position)
        self.last_result = Symbol(left == right)

    def do_for_inequality_expr(self, node: InequalityExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if type(left) is not type(right):
            raise MismatchedTypesError(node.position)
        self.last_result = Symbol(left != right)

    def do_for_addition_expr(self, node: AdditionExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left + right)

    def do_for_subtraction_expr(self, node: SubtractionExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left - right)

    def do_for_multiplication_expr(self, node: MultiplicationExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left * right)

    def do_for_division_expr(self, node: DivisionExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if right == 0:
            raise DivisionByZeroError(node.position)
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )

        self.last_result = Symbol(left / right)

    def do_for_power_expr(self, node: PowerExpression):
        node.left.accept_visitor(self)
        left = self.last_result.get_value()
        node.right.accept_visitor(self)
        right = self.last_result.get_value()
        if not isinstance(left, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(left).__name__
            )
        if not isinstance(right, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(right).__name__
            )
        self.last_result = Symbol(left ** right)

    def do_for_not_expr_logical(self, node: NotExpressionLogical):
        node.term.accept_visitor(self)
        factor = self.last_result.get_value()
        if not isinstance(factor, bool):
            raise InvalidTypeError(
                node.position,
                'boolean',
                type(factor).__name__
            )
        self.last_result = Symbol(not factor)

    def do_for_not_expr_aritmetic(self, node: NotExpressionAritmetic):
        node.term.accept_visitor(self)
        factor = self.last_result.get_value()
        if not isinstance(factor, (int, float)):
            raise InvalidTypeError(
                node.position,
                'number',
                type(factor).__name__
            )
        self.last_result = Symbol(-factor)

    def do_for_term(self, node: Term):
        self.last_result = Symbol(node.value)

    def interpret(self, program):
        program.accept_visitor(self)
