import io
import pytest

from src.error_handling.interpreter_error import (
    DivisionByZeroError,
    FunctionRedefinitionError,
    IndexOutOfRangeError,
    InvalidIndexError,
    InvalidTypeError,
    InvalidVariableAssignmentError,
    IterableNameError,
    MismatchedTypesError,
    NonExistingAttributeError,
    NonExistingMethodError,
    NonExistingVariableError,
    NonExistingFunctionError,
    BreakOutsideLoopError,
    InvalidConstructorArgumentsError,
    InvalidFunCallArgumentsError,
    InvalidNumberOfArgumentsError,
    RecursionLimitError,
    ReturnOutsideFunctionError,
    TypeCastingError,
    VariableRedeclarationError
)
from src.interpreter.symbol_table import Circle, Square
from src.parser.parser import Parser
from src.constants import (
    MAXIMUM_FLOAT_DECIMALS,
    MAXIMUM_IDENTIFIER,
    MAXIMUM_INT_DIGITS,
    MAXIMUM_STRING,
    MAXIMUM_RECURSION_DEPTH
)
from src.interpreter.interpreter import Interpreter
from src.lexer.lexer import Lexer
from src.lexer.stream import Stream


class TestInterpreter:
    def init_parser(self, text):
        lexer = Lexer(
            Stream(io.StringIO(text)),
            MAXIMUM_IDENTIFIER,
            MAXIMUM_STRING,
            MAXIMUM_INT_DIGITS,
            MAXIMUM_FLOAT_DECIMALS,
        )
        parser = Parser(lexer)
        return parser

    def interpret(self, text):
        parser = self.init_parser(text)
        program = parser.parse_program()
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.visit(program)
        return interpreter

    def test_get_variable(self):
        text = 'var a = 1;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1

        text = 'var a = 1; a = a + 1;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 2

        text = 'var a_list = [1, 2, 3];'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a_list').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [1, 2, 3]

        text = 'var a_list = [1, 2, 3]; a_list[0] = 4;'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a_list').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [4, 2, 3]

        text = 'var a_list = [1, 2, 3]; a_list[0 + 1] = 0;'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a_list').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [1, 0, 3]

        text = 'var a = [0, 1, 2]; var b = [3, 4, 5]; var c = [a, b];'
        text += 'var d = c[1][1];'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('d').get_value() == 4

        text = 'a = 1;'
        with pytest.raises(NonExistingVariableError):
            interpreter = self.interpret(text)

        text = 'var a_list = [1, 2, 3]; a_list[3] = 4;'
        with pytest.raises(IndexOutOfRangeError):
            interpreter = self.interpret(text)

        text = 'var a_list = [1, 2, 3]; a_list[3.0] = 4;'
        with pytest.raises(InvalidIndexError):
            interpreter = self.interpret(text)

        text = 'var a = 0; var a = 1;'
        with pytest.raises(VariableRedeclarationError):
            interpreter = self.interpret(text)

    def test_function_call(self):
        text = 'print("Hello, World!");'
        interpreter = self.interpret(text)
        assert interpreter.last_result is None

        text = 'var i = 1; var s = str(i);'
        interpreter = self.interpret(text)
        assert type(interpreter.current_scope().get('s').get_value()) == str

        text = 'var s = "1"; var i = int(s);'
        interpreter = self.interpret(text)
        assert type(interpreter.current_scope().get('i').get_value()) == int

        text = 'var s = "string"; var i = int(s);'
        with pytest.raises(TypeCastingError):
            interpreter = self.interpret(text)

        text = 'var i = 3; var j = 2; float(i, j);'
        with pytest.raises(InvalidNumberOfArgumentsError):
            interpreter = self.interpret(text)

        text = 'def foo(){return 1;} var a = foo();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1

        text = 'def foo(a){a = a + 1; return a;} var c = 1; var b = foo(c);'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('c').get_value() == 1
        assert interpreter.current_scope().get('b').get_value() == 2

        text = 'def foo(){return 1;} var a = [foo(), 2, 3];'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [1, 2, 3]

        text = 'def foo(a){return a;} var b = 1; var c = foo(b);'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('c').get_value() == 1

        text = 'def foo(a){return a;} var result = foo();'
        with pytest.raises(InvalidNumberOfArgumentsError):
            interpreter = self.interpret(text)

        text = 'def foo(a){return a; a = 0;} var result = foo(1);'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('result').get_value() == 1

        text = 'def foo(a){a = a + 1; return a; a = 0;} var b = foo(0);'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('b').get_value() == 1

        text = '2 + 3; def foo(){return;} var a = foo();'
        with pytest.raises(InvalidVariableAssignmentError):
            interpreter = self.interpret(text)

        text = 'var a = foo();'
        with pytest.raises(NonExistingFunctionError):
            interpreter = self.interpret(text)

        text = 'print(3);'
        with pytest.raises(InvalidFunCallArgumentsError):
            interpreter = self.interpret(text)

        text = 'var a = 1; return;'
        with pytest.raises(ReturnOutsideFunctionError):
            interpreter = self.interpret(text)

        text = 'def foo(){return;} def foo(a){return a;}'
        with pytest.raises(FunctionRedefinitionError):
            interpreter = self.interpret(text)

        text = 'def foo(){foo();} var a = foo();'
        with pytest.raises(RecursionLimitError):
            interpreter = self.interpret(text)

    def test_constructors(self):
        text = 'var p = Point(1, 2);'
        interpreter = self.interpret(text)
        p = interpreter.current_scope().get('p').get_value()
        assert p.attributes['x'].get_value() == 1

        text = 'var s = Square(Point(1, 2), 3);'
        interpreter = self.interpret(text)
        square = interpreter.current_scope().get('s').get_value()
        square_position = square.attributes['position'].get_value()
        assert square_position.attributes['x'].get_value() == 1
        assert square.attributes['side'].get_value() == 3

        text = 'var s = Square(Point("1", "2"), 3);'
        with pytest.raises(InvalidConstructorArgumentsError):
            interpreter = self.interpret(text)

        text = 'var s = Square(Point(1), 3);'
        with pytest.raises(InvalidNumberOfArgumentsError):
            interpreter = self.interpret(text)

        text = 'var s = Square(1, 3);'
        with pytest.raises(InvalidConstructorArgumentsError):
            interpreter = self.interpret(text)

        text = 'var s = Square(Point(1, 2), 3);'
        text += 'var c = Circle(Point(1, 2), 3);'
        text += 'var scene = Scene([s, c]);'
        interpreter = self.interpret(text)
        scene = interpreter.current_scope().get('scene').get_value()
        for obj in scene.attributes['figures'].get_value():
            assert type(obj.get_value()) in [Square, Circle]

    def test_if_else(self):
        text = 'def bar(){var a=5; if(a>0){var b=10; a=a+b;} return a;}'
        text += 'var result=bar();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('result').get_value() == 15

        text = 'var z=30; def baz(){var z=40; if(True){z=50;} return z;}'
        text += 'var result=baz();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('result').get_value() == 50
        assert interpreter.current_scope().get('z').get_value() == 30

        text = 'var z=30; def baz(){var z=40; if(True){var z=50;} return z;}'
        text += 'var result=baz();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('result').get_value() == 40
        assert interpreter.current_scope().get('z').get_value() == 30

        text = 'var a = 0; if( a > 0){ a = 1;} else{ a = 2;}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 2

    def test_while_loop(self):
        text = 'var a = 0; while(a < 5){ a = a + 1;}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 5

        text = 'var a = 0; while(a < 5){ a = a + 1;} var b = a;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('b').get_value() == 5

        text = 'var a = 0; while(True){ a = a + 1; if(a == 5){ break;}}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 5

        text = 'def foo(){'
        text += 'var i = 0;'
        text += 'while(i<3){var j=0;'
        text += 'while(j<3){ if (i == 1 && j == 1){ return i;} j=j+1;} i=i+1;}'
        text += '}'
        text += 'var a = foo();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1

        text = 'var a = 1; var b = 0;'
        text += 'while(a < 3){ while(b < 5){ b = b + a;} a = a + 1;}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 3
        assert interpreter.current_scope().get('b').get_value() == 5

        text = 'var a = 0; break;'
        with pytest.raises(BreakOutsideLoopError):
            interpreter = self.interpret(text)

        text = 'def foo(){var a = 0; while(a < 5){ a = a + 1;}}'
        text += 'var b = foo(); break;'
        with pytest.raises(BreakOutsideLoopError):
            interpreter = self.interpret(text)

    def test_for_loop(self):
        text = 'var a = [0, 1, 2]; for(i in a){ a[i] = a[i] + 1;}'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [1, 2, 3]

        text = 'var sum = 0; var a = [1, 2, 3]; for(i in a){ sum = sum + i;}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('sum').get_value() == 6

        text = 'var sum = 0; for (i in [1, 2, 3]){ sum = sum + i;}'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('sum').get_value() == 6

        text = 'var a = [0, 1, 2]; for(i in a){ a[i] = 0;}'
        interpreter = self.interpret(text)
        a_list = interpreter.current_scope().get('a').get_value()
        val_list = []
        for val in a_list:
            val_list.append(val.get_value())
        assert val_list == [0, 0, 0]

        text = 'var a = [0, 1, 2]; for(i in a){ a = 0;} i = 0;'
        with pytest.raises(NonExistingVariableError):
            interpreter = self.interpret(text)

        text = 'var i = 0; for(i in [1, 2, 3]){ i = i + 1;}'
        with pytest.raises(IterableNameError):
            interpreter = self.interpret(text)

    def test_dot_access(self):
        text = 'var point = Point(1, 2); var x = point.get_x();'
        interpreter = self.interpret(text)
        point = interpreter.current_scope().get('point').get_value()
        assert point.attributes['x'].get_value() == 1
        assert interpreter.current_scope().get('x').get_value() == 1

    def test_attribute_access(self):
        text = 'var point = Point(1, 2);'
        text += 'var square = Square(point, 3); square.side = 4;'
        interpreter = self.interpret(text)
        square = interpreter.current_scope().get('square').get_value()
        square_position = square.attributes['position'].get_value()
        assert square_position.attributes['x'].get_value() == 1
        assert square_position.attributes['y'].get_value() == 2
        assert square.attributes['side'].get_value() == 4

        text = 'var point = Point(1, 2);'
        text += 'var square = Square(point, 3); square.side = 4;'
        interpreter = self.interpret(text)
        square = interpreter.current_scope().get('square').get_value()
        square_position = square.attributes['position'].get_value()
        assert square_position.attributes['x'].get_value() == 1
        assert square_position.attributes['y'].get_value() == 2
        assert square.attributes['side'].get_value() == 4

        text = 'var point = Point(1, 2); var attribute = point.attribute;'
        with pytest.raises(NonExistingAttributeError):
            interpreter = self.interpret(text)

        text = 'var point = Point(1, 2); var x = point.x;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('x').get_value() == 1

    def test_method_call(self):
        text = 'var square = Square(Point(0, 0), 3); var area = square.area();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('area').get_value() == 9

        text = 'var square = Square(Point(0, 0), 3);'
        text += 'var circ = square.perimeter();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('circ').get_value() == 12

        text = 'var square = Square(Point(0, 0), 3);'
        text += 'var x = square.position.get_x();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('x').get_value() == 0

        text = 'var square = Square(Point(0, 0), 3); square.method();'
        with pytest.raises(NonExistingMethodError):
            interpreter = self.interpret(text)

        text = 'var rectangle = Rectangle(Point(1, 1), 3, 2);'
        text += 'rectangle.move_to(Point(2, 2));'
        text += 'var x = rectangle.position.get_x();'
        text += 'var y = rectangle.position.get_y();'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('x').get_value() == 2
        assert interpreter.current_scope().get('y').get_value() == 2

        text = 'var point = Point(1, 2); point.set_x(3);'
        interpreter = self.interpret(text)
        point = interpreter.current_scope().get('point').get_value()
        assert point.attributes['x'].get_value() == 3

        text = 'var point = Point(1, 2); point.set_x(1, 2);'
        with pytest.raises(InvalidNumberOfArgumentsError):
            interpreter = self.interpret(text)

        text = 'var point = Point(1, 2); point.set_x("string");'
        with pytest.raises(InvalidFunCallArgumentsError):
            interpreter = self.interpret(text)

        text = 'var square = Square(Point(0, 0), 3); square.side="string";'
        text += 'var area = square.area();'
        with pytest.raises(InvalidFunCallArgumentsError):
            interpreter = self.interpret(text)

        text = 'var rhomb = Rhomb(Point(0, 0), 3, 4);'
        text += 'rhomb.side = "string";'
        text += 'var scene = Scene([rhomb]); scene.render();'
        with pytest.raises(InvalidFunCallArgumentsError):
            interpreter = self.interpret(text)

    def test_expressions(self):
        text = 'if(1 or 2){var a = 1;}'
        with pytest.raises(InvalidTypeError):
            self.interpret(text)

        text = 'if(1 and True){var a = 1;}'
        with pytest.raises(InvalidTypeError):
            self.interpret(text)

        text = 'var a = 1 + 2;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 3

        text = 'var a = 1 - 2;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == -1

        text = 'var a = 1 * 2;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 2

        text = 'var a = 1 / 2;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 0.5

        text = 'var a = 1 + 2 * 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 7

        text = 'var a = (1 + 2) * 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 9

        text = 'var a = 1 + 2 / 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1 + 2 / 3

        text = 'var a = 1 - 2 * 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1 - 2 * 3

        text = 'var a = 1 - 2 / 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1 - 2 / 3

        text = 'var a = 1 * 2 / 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 1 * 2 / 3

        text = 'var a = (2 + 3) * (4 - 5) / 2;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == (
            (2 + 3) * (4 - 5) / 2
        )

        text = 'var a = 4 * 2 ** 3;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() == 4 * 2 ** 3

        text = 'var a = True or (False and (not True));'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is True

        text = 'var a = (2 + 3) * 4 > 10 and not (4 / 2 == 2.0);'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is False

        text = 'var a =  3 ** 2 == 9 or (5 - 3) * 2 < 5;'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is True

        text = 'var a = not (((5 + (3 * 2)) < 10) and ((4 / 2) ** 2 != 4.0));'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is True

        text = 'var a = 1 + "string";'
        with pytest.raises(InvalidTypeError):
            interpreter = self.interpret(text)

        text = 'var a = "string" == "string";'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is True

        text = 'var a = "string" != "string";'
        interpreter = self.interpret(text)
        assert interpreter.current_scope().get('a').get_value() is False

        text = 'var a = 1 == "1";'
        with pytest.raises(MismatchedTypesError):
            interpreter = self.interpret(text)

        text = '1 / 0;'
        with pytest.raises(DivisionByZeroError):
            interpreter = self.interpret(text)
