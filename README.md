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
