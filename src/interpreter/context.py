from src.error_handling.interpreter_error import (
    BaseForInvalidConstructorArgumentsError,
    BaseForInvalidFunCallArgumentsError,
    BaseForTypeCastingError
)
from src.interpreter.symbol_table import (
    Circle,
    Parallelogram,
    Rhomb,
    Symbol,
    Point,
    Square,
    Scene,
    Rectangle,
    Triangle,
    Trapeze
)


class Scope:
    def __init__(self, parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        if name in self.symbols:
            del self.symbols[name]


class Context:
    def __init__(self, global_scope):
        self.scope_stack = [Scope(parent=global_scope)]
        self.while_loop_counter = 0


class GlobalContext:
    def __init__(self, global_scope):
        self.scope_stack = [global_scope]
        self.while_loop_counter = 0
        self.functions = {
            'print': print_function,
            'str': str_cast,
            'int': int_cast,
            'float': float_cast,
            'Point': point_constructor,
            'Square': square_constructor,
            'Rectangle': rectangle_constructor,
            'Circle': circle_constructor,
            'Triangle': triangle_constructor,
            'Rhomb': rhomb_constructor,
            'Parallelogram': parallelogram_constructor,
            'Trapeze': trapeze_constructor,
            'Scene': scene_constructor
        }

    def get_embedded_function(self, name):
        if name in self.embedded_functions:
            return self.embedded_functions[name]
        else:
            return None

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            return None

    def set_function(self, name, function):
        self.functions[name] = function


class Function:
    def __init__(self, body):
        self.body = body


class UserFunction(Function):
    def __init__(self, parameters, body):
        super().__init__(body)
        self.parameters = parameters

    def accept_visitor(self, visitor):
        visitor.do_for_user_function(self)


class EmbeddedFunction(Function):
    def __init__(self, body, number_of_parameters=None):
        super().__init__(body)
        self.number_of_parameters = number_of_parameters

    def accept_visitor(self, visitor):
        visitor.do_for_embedded_function(self)


def do_for_print(arguments):
    string = ''
    for arg in arguments:
        if isinstance(arg, str) is False:
            raise BaseForInvalidFunCallArgumentsError('print')
        string += arg
    print(string)


def do_for_point(arguments):
    if (
        isinstance(arguments[0], (int, float)) is False or
        isinstance(arguments[1], (int, float)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Point')
    return Symbol(Point(arguments))


def do_for_square(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], int) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Square')
    return Symbol(Square(arguments))


def do_for_rectangle(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], (int, float)) is False or
        isinstance(arguments[2], (int, float)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Rectangle')
    return Symbol(Rectangle(arguments))


def do_for_circle(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], (int, float)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Circle')
    return Symbol(Circle(arguments))


def do_for_triangle(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], Point) is False or
        isinstance(arguments[2], Point) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Triangle')
    return Symbol(Triangle(arguments))


def do_for_rhomb(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], (int, float)) is False or
        isinstance(arguments[2], (int)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Rhomb')
    return Symbol(Rhomb(arguments))


def do_for_parallelogram(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], (int, float)) is False or
        isinstance(arguments[2], (int, float)) is False or
        isinstance(arguments[3], (int)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Parallelogram')
    return Symbol(Parallelogram(arguments))


def do_for_trapeze(arguments):
    if (
        isinstance(arguments[0], Point) is False or
        isinstance(arguments[1], (int, float)) is False or
        isinstance(arguments[2], (int, float)) is False or
        isinstance(arguments[3], (int, float)) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Trapeze')
    return Symbol(Trapeze(arguments))


def do_for_scene(arguments):
    if (
        isinstance(arguments[0], list) is False
    ):
        raise BaseForInvalidConstructorArgumentsError('Scene')
    for arg in arguments[0]:
        if (
            isinstance(arg.get_value(), (
                Square,
                Rectangle,
                Circle,
                Triangle,
                Rhomb,
                Parallelogram,
                Trapeze
            )) is False
        ):
            raise BaseForInvalidConstructorArgumentsError('Scene')
    return Symbol(Scene(arguments))


def do_for_str(arguments):
    try:
        return Symbol(str(arguments[0]))
    except ValueError:
        raise BaseForTypeCastingError('str')


def do_for_int(arguments):
    try:
        return Symbol(int(arguments[0]))
    except ValueError:
        raise BaseForTypeCastingError('int')


def do_for_float(arguments):
    try:
        return Symbol(float(arguments[0]))
    except ValueError:
        raise BaseForTypeCastingError('float')


print_function = EmbeddedFunction(do_for_print)
point_constructor = EmbeddedFunction(do_for_point, 2)
square_constructor = EmbeddedFunction(do_for_square, 2)
rectangle_constructor = EmbeddedFunction(do_for_rectangle, 3)
circle_constructor = EmbeddedFunction(do_for_circle, 2)
triangle_constructor = EmbeddedFunction(do_for_triangle, 3)
rhomb_constructor = EmbeddedFunction(do_for_rhomb, 3)
parallelogram_constructor = EmbeddedFunction(do_for_parallelogram, 4)
trapeze_constructor = EmbeddedFunction(do_for_trapeze, 4)
scene_constructor = EmbeddedFunction(do_for_scene, 1)
str_cast = EmbeddedFunction(do_for_str, 1)
int_cast = EmbeddedFunction(do_for_int, 1)
float_cast = EmbeddedFunction(do_for_float, 1)
