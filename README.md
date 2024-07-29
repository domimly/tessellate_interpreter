# Tessellate -- Language for Describing Geometric Figures.

## Project goal.
The goal of the project is to create a programming language that will enable the description of geometric figures and their properties, as well as to display a scene composed of them on the screen.

## Basic assumptions.
Tessellate supports basic data types such as `int`, `float`, `string`, and `bool`. Additionally, it has built-in types specific to the description of geometric figures.\
The language allows for variable declarations, defining custom functions, and provides conditional statements, loops, and comments.\
Mathematical operation precedence is preserved, along with parentheses for grouping.\
The language has dynamic and strong typing.\
It does not provide automatic type conversion, but it does provide functions for casting variables (e.g., `int` to `float`, `int` or `float` to `string`).\
Variables are mutable -- a value can be assigned to a variable multiple times.\
Parameters are passed to functions by value.\
The language does not require a `main` function to be implemented to run a program, it will start execution from the first line of the file.

## Data types.
### Basic data types.
- `int`
```
var a = 5;
```

- `float`
```
var b = 3.14;
```

- `string`
Begins and ends with single or double quotes.
```
var string1 = "Hello World!";
var string2 = 'Hello World!';
```
- `bool`
Can be either True or False.
```
var t = True;
var f = False;
```

### Other, Tessellate specific data types.

- `Point`
```
var point = Point(0, 0);

point.set_x(1);
point.set_y(2);

var x = point.get_x();      # 1
var y = point.get_y();      # 2

print('x: ', str(x));
print('y: ', str(y));

# expected output:
# x: 1
# y: 2
```

- `Rectangle`
```
var rectangle = Rectangle(Point(1, 1), 3, 2);

rectangle.set_width(4);
rectangle.set_height(5);

var w = rectangle.get_width();          # 4
var h = rectangle.get_height();         # 5

var area = rectangle.area();
var perimeter = rectangle.perimeter();
var diagonal = rectangle.diagonal();

print('width: ', str(w));
print('height: ', str(h));
print('area: ' str(area));
print('perimeter: ', str(perimeter));
print('diagonal: ', str(diagonal));

# expected output:
# width: 4
# height: 5
# area: 20
# perimeter: 18
# diagonal: 6.4031242374328485
```

- `Square`
```
var square = Square(Point(1, 1), 5);

square.set_side(2);

var s = square.get_side();      # 2

var area = square.area();
var perimeter = square.perimeter();
var diagonal = square.diagonal();

print('side: ', str(s));
print('area: ', str(area));
print('perimeter: ', str(perimeter));
print('diagonal: ', str(diagonal));

# expected output:
# side: 2
# area: 4
# perimeter: 8
# diagonal: 2.8284271247461903
```

- `Triangle`
```
var triangle = Triangle(Point(1, 2), Point(3, 1), Point(2, 3));

triangle.set_point1(Point(1, 1));

var p1 = triangle.get_point1();

var area = triangle.area();
var perimeter = triangle.perimeter();
var sides = triangle.sides();
var heights = triangle.heights();

print('point1 x: ', str(triangle.point1.get_x()));
print('point1 y: ', str(triangle.point1.get_y()));
print('area: ', str(area));
print('perimeter: ', str(perimeter));
print('sides: ');
for (side in sides){
    print(str(side));
}
print('heights: ');
for (height in heights){
    print(str(height));
}

# expected output:
# point1 x: 1
# point1 y: 1
# area: 2.0
# perimeter: 6.47213595499958
# sides: 
# 2.0
# 2.23606797749979
# 2.23606797749979
# heights: 
# 2.0
# 1.7888543819998317
# 1.7888543819998317
```

- `Circle`
```
var circle = Circle(Point(5, 5), 2);

circle.set_radius(3);

var r = circle.get_radius();      # 3

var area = circle.area();
var perimeter = circle.perimeter();
var diameter = circle.diameter();

print('radius: ', str(r));
print('area: ', str(area));
print('perimeter: ', str(perimeter));
print('diameter: ', str(diameter));

# expected output:
# radius: 3
# area: 28.259999999999998
# perimeter: 18.84
# diameter: 6
```

- `Rhomb`
```
var rhomb = Rhomb(Point(1, 1), 5, 30);

rhomb.set_side(3);
rhomb.set_angle(60);

var s = rhomb.get_side();       # 3
var a = rhomb.get_angle();      # 60

var area = rhomb.area();
var perimeter = rhomb.perimeter();
var diagonals = rhomb.diagonals();

print('side: ', str(s));
print('angle: ', str(a));
print('area: ', str(area));
print('perimeter: ', str(perimeter));
print('diagonals: ');
for (d in diagonals){
    print(str(d));
}

# expected output:
# side: 3
# angle: 60
# area: 7.794228634059947
# perimeter: 12
# diagonals: 
# 5.196152422706632
# 2.9999999999999996
```
- `Parallelogram`
```
var parallelogram = Parallelogram(Point(1, 1), 10, 5, 60);

parallelogram.set_base(8);
parallelogram.set_height(6);
parallelogram.set_angle(45);

var s = parallelogram.get_base();       # 8
var h = parallelogram.get_height();     # 6
var a = parallelogram.get_angle();      # 45

var area = parallelogram.area();
var perimeter = parallelogram.perimeter();
var sides = parallelogram.sides();
var diagonals = parallelogram.diagonals();

print('sides: ');
for (side in sides){
    print(str(side));
}
print('angle: ', str(a));
print('area: ', str(area));
print('perimeter: ', str(perimeter));
print('diagonals: ');
for (d in diagonals){
    print(str(d));
}

# expected output:
# sides: 
# 8
# 8.485281374238571
# angle: 45
# area: 48
# perimeter: 32.97056274847714
# diagonals: 
# 15.231546211727817
# 6.324555320336757
```

- `Trapeze`
```
var trapeze = Trapeze(Point(2, 2), 10, 8, 6);

trapeze.set_base1(8);
trapeze.set_base2(6);
trapeze.set_height(4);

var b1 = trapeze.get_base1();       # 8
var b2 = trapeze.get_base2();       # 6
var h = trapeze.get_height();       # 4

var area = trapeze.area();
var perimeter = trapeze.perimeter();

print('base1: ', str(b1));
print('base2: ', str(b2));
print('height: ', str(h));
print('area: ', str(area));
print('perimeter: ', str(perimeter));

# expected output:
# base1: 8
# base2: 6
# height: 4
# area: 28.0
# perimeter: 26.18536337391621
```

## Tessellate grammar.
Below is the grammar of Tessellate in EBNF:
```
program                     ::= {statement};

statement                   ::= block_statement | function_definition;

block_statement             ::= assignment_statement_or_object
                            | variable_declaration
                            | break_statement
                            | return_statement
                            | if_statement
                            | while_statement
                            | for_statement
                            | expression;

variable_declaration        ::= "var", identifier, "=", expression, ";";

assignment_statement_or_object
                            ::= identifier, {".", object} ["=", expression], ';';

break_statement             ::= 'break', ';';

return_statement            ::= 'return', [expression], ';';

operation_block             ::= "{", {block_statement}, "}";

if_statement                ::= "if", "(", expression, ")", operation_block,
                              ["else", operation_block];

while_statement             ::= "while", "(", expression, ")", operation_block;

for_statement               ::= "for", "(", identifier, "in", identifier | list, ")", operation_block;

function_definition         ::= "def", identifier, parameter_list, operation_block;

object                      ::= identifier, [argument_list | list_index];

identifier                  ::= letter {letter | digit | "_"};

list                        ::= "[", [expression, {",", expression}], "]";

parameter_list              ::= "(", [identifier, {",", identifier}], ")";

argument_list               ::= "(", [expression, {",", expression}], ")";

list_index                  ::= "[", expression, "]";

expression                  ::= and_expression, {or_operator, and_expression};

and_expression              ::= relation_expression, {and_operator, relation_expression};

relation_expression         ::= add_expression, [ relation_operator, add_expression ];

add_expression              ::= multiply_expression, { add_operator, multiply_expression };

multiply_expression         ::= power_expression, { multiply_operator, power_expression};

power_expression            ::= not_expression, { "**", not_expression};

not_expression              ::= [not_operator], term;

term                        ::= int
                            | float
                            | bool
                            | string
                            | object
                            | list
                            | '(' expression ')';

add_operator                ::= "+" | "-";

multiply_operator           ::= "*" | "/";

relation_operator           ::= "=="
                            | "!="
                            | ">"
                            | "<"
                            | ">="
                            | "<="

not_operator                ::= "not" | "!" | "-";

or_operator                 ::= "or" | "||"

and_operator                ::= "and" | "&&"

number                      ::= int | float;

int                         ::= "0" | non_zero_digit, {digit};

float                       ::= "0", ".", digit, {digit} | non_zero_digit, {digit}, ".", digit, {digit};

string                      ::= '"' {character} '"' | "'" {character} "'";

letter                      ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z";

non_zero_digit              ::= "1" | ... | "9";

digit                       ::= "0" | non_zero_digit;

bool                        ::= "True" | "False";
```
