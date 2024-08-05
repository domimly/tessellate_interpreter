class InterpreterError(Exception):
    def __str__(self):
        return f'\n\nInterpreter Error: {self.message} {self.position}'


class NonExistingVariableError(InterpreterError):
    def __init__(self, position, var_name):
        self.message = f'Tried to access non-existing variable: {var_name}'
        self.position = position


class InvalidVariableAssignmentError(InterpreterError):
    def __init__(self, position, var_name):
        self.message = (
            f'Invalid variable assignment for: {var_name}, ' +
            'variable cannot be assigned an empty value'
        )
        self.position = position


class NonExistingAttributeError(InterpreterError):
    def __init__(self, position, attr_name, object_name):
        self.message = (
            f'Tried to access non-existing attribute: {attr_name} ' +
            f'for object: {object_name}'
        )
        self.position = position


class NonExistingFunctionError(InterpreterError):
    def __init__(self, position, func_name):
        self.message = f'Tried to access a non-defined function: {func_name}'
        self.position = position


class NonExistingMethodError(InterpreterError):
    def __init__(self, position, method_name, object_name):
        self.message = (
            f'Tried to access a non-defined method: {method_name} ' +
            f'for object: {object_name}'
        )
        self.position = position


class InvalidNumberOfArgumentsError(InterpreterError):
    def __init__(self, position, func_name, expected, got):
        self.message = (
            f'Invalid number of arguments for function {func_name} ',
            f'Expected {expected}, got {got}'
        )
        self.position = position


class TypeCastingError(InterpreterError):
    def __init__(self, position, type_name, got):
        self.message = (
            f'Invalid type casting -- cannot cast {got} to {type_name}'
        )
        self.position = position


class InvalidConstructorArgumentsError(InterpreterError):
    def __init__(self, position, class_name):
        self.message = (
            f'Invalid constructor arguments for class {class_name}'
        )
        self.position = position


class InvalidFunCallArgumentsError(InterpreterError):
    def __init__(self, position, func_name):
        self.message = (
            f'Invalid arguments for function call {func_name}'
        )
        self.position = position


class BreakOutsideLoopError(InterpreterError):
    def __init__(self, position):
        self.message = 'Break statement outside of loop'
        self.position = position


class ReturnOutsideFunctionError(InterpreterError):
    def __init__(self, position):
        self.message = 'Return statement outside of function'
        self.position = position


class UnsuccessfulFunCallError(InterpreterError):
    def __init__(self, position, func_name):
        self.message = f'Unsuccessful attempt to call function: {func_name}'
        self.position = position


class IndexOutOfRangeError(InterpreterError):
    def __init__(self, position, list_name):
        self.message = (
            f'Index out of range for list: {list_name}'
        )
        self.position = position


class InvalidIndexError(InterpreterError):
    def __init__(self, position, list_name, index_type):
        self.message = (
            f'Invalid index for list: {list_name} --' +
            f'expected type of index: int, got: {index_type}'
        )
        self.position = position


class IterableNameError(InterpreterError):
    def __init__(self, position, iter_name):
        self.message = (
            f'Variable with name: {iter_name} already exists in this scope, ' +
            'name of item to iterate over must be unique'
        )
        self.position = position


class FunctionRedefinitionError(InterpreterError):
    def __init__(self, position, func_name):
        self.message = (
            f'Function with name: {func_name} already exists, ' +
            'name of function must be unique'
        )
        self.position = position


class VariableRedeclarationError(InterpreterError):
    def __init__(self, position, var_name):
        self.message = (
            f'Variable with name: {var_name} already exists in this scope, ' +
            'name of variable must be unique'
        )
        self.position = position


class InvalidTypeError(InterpreterError):
    def __init__(self, position, expected, got):
        self.message = (
            f'Invalid type, expected: {expected}, got: {got}'
        )
        self.position = position


class MismatchedTypesError(InterpreterError):
    def __init__(self, position):
        self.message = (
            'Mismatched types of operands in operation'
        )
        self.position = position


class RecursionLimitError(InterpreterError):
    def __init__(self, position, func_name):
        self.message = (
            'Recursion limit exceeded for function: {func_name}'
        )
        self.position = position


class DivisionByZeroError(InterpreterError):
    def __init__(self, position):
        self.message = (
            'Division by zero'
        )
        self.position = position


class BaseForTypeCastingError(Exception):
    def __init__(self, type_name, got=None):
        self.type_name = type_name
        self.got = got


class BaseForInvalidConstructorArgumentsError(Exception):
    def __init__(self, class_name):
        self.class_name = class_name


class BaseForInvalidFunCallArgumentsError(Exception):
    def __init__(self, fun_name):
        self.fun_name = fun_name


class BaseForInvalidNumberOfArgumentsError(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got
