from src.interpreter.interpreter import Interpreter
from src.constants import MAXIMUM_RECURSION_DEPTH
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
    TermType,
    VariableAssignment,
    WhileStatement,
    Parameter,
)

POS = [1, 0]


class TestInterpreter:
    def test_variables(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    Term(POS, TermType.INT, 2)
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 1
        assert interpreter.current_scope().get('b').get_value() == 2

    def test_assignment(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                Assignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 2)
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 2

    def test_if_statement(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                IfStatement(
                    POS,
                    LessThanExpression(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 2)
                    ),
                    Assignment(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 2)
                    ),
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 2

    def test_if_else_statement(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                IfStatement(
                    POS,
                    LessThanExpression(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 0)
                    ),
                    Assignment(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 2)
                    ),
                    Assignment(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 3)
                    ),
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 3

    def test_while_statement(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 0)
                ),
                WhileStatement(
                    POS,
                    LessThanExpression(
                        POS,
                        Identifier(POS, 'a'),
                        Term(POS, TermType.INT, 3)
                    ),
                    Assignment(
                        POS,
                        Identifier(POS, 'a'),
                        AdditionExpression(
                            POS,
                            Identifier(POS, 'a'),
                            Term(POS, TermType.INT, 1)
                        )
                    ),
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 3

    def test_for_each_statement(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    List(
                        POS,
                        [
                            Term(POS, TermType.INT, 1),
                            Term(POS, TermType.INT, 2),
                            Term(POS, TermType.INT, 3),
                        ]
                    )
                ),
                ForStatement(
                    POS,
                    'i',
                    Identifier(POS, 'a'),
                    Assignment(
                        POS,
                        Identifier(POS, 'i'),
                        AdditionExpression(
                            POS,
                            Identifier(POS, 'i'),
                            Term(POS, TermType.INT, 1)
                        )
                    ),
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        a_list = interpreter.current_scope().get('a').get_value()
        for i in range(0, 3):
            a_list[i].get_value() == i + 1

    def test_aritmetic_expressions(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    AdditionExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    SubtractionExpression(
                        POS,
                        Term(POS, TermType.INT, 3),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'c'),
                    MultiplicationExpression(
                        POS,
                        Term(POS, TermType.INT, 2),
                        Term(POS, TermType.INT, 3)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'd'),
                    DivisionExpression(
                        POS,
                        Term(POS, TermType.INT, 6),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'e'),
                    PowerExpression(
                        POS,
                        Term(POS, TermType.INT, 2),
                        Term(POS, TermType.INT, 3)
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 3
        assert interpreter.current_scope().get('b').get_value() == 1
        assert interpreter.current_scope().get('c').get_value() == 6
        assert interpreter.current_scope().get('d').get_value() == 3
        assert interpreter.current_scope().get('e').get_value() == 8

    def test_logical_expressions(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    OrExpression(
                        POS,
                        Term(POS, TermType.BOOL, True),
                        Term(POS, TermType.BOOL, False)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    AndExpression(
                        POS,
                        Term(POS, TermType.BOOL, True),
                        Term(POS, TermType.BOOL, False)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'c'),
                    LessThanExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'd'),
                    GreaterThanExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'e'),
                    LessOrEqualExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'f'),
                    GreaterOrEqualExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'g'),
                    EqualityExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'h'),
                    InequalityExpression(
                        POS,
                        Term(POS, TermType.INT, 1),
                        Term(POS, TermType.INT, 2)
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() is True
        assert interpreter.current_scope().get('b').get_value() is False
        assert interpreter.current_scope().get('c').get_value() is True
        assert interpreter.current_scope().get('d').get_value() is False
        assert interpreter.current_scope().get('e').get_value() is True
        assert interpreter.current_scope().get('f').get_value() is False
        assert interpreter.current_scope().get('g').get_value() is False
        assert interpreter.current_scope().get('h').get_value() is True

    def test_not_expressions(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    NotExpressionLogical(
                        POS,
                        Term(POS, TermType.BOOL, True)
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    NotExpressionAritmetic(
                        POS,
                        Term(POS, TermType.INT, 1)
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() is False
        assert interpreter.current_scope().get('b').get_value() == -1

    def test_list(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    List(
                        POS,
                        [
                            Term(POS, TermType.INT, 1),
                            Term(POS, TermType.INT, 2),
                            Term(POS, TermType.INT, 3),
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    ListIndexAccess(
                        POS,
                        'a',
                        [ListIndex(POS, Term(POS, TermType.INT, 1))]
                    )
                ),

            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        a_list = interpreter.current_scope().get('a').get_value()
        for i in range(0, 3):
            a_list[i].get_value() == i + 1
        assert interpreter.current_scope().get('b').get_value() == 2

    def test_function_definition(self):
        program = Program(
            POS,
            [
                FunctionDefinition(
                    POS,
                    'f',
                    [],
                    OperationBlock(
                        POS,
                        [
                            ReturnStatement(
                                POS,
                                Term(POS, TermType.INT, 1)
                            )
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    FunCall(
                        POS,
                        'f',
                        []
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 1

    def test_break_statement(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 0)
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'i'),
                    Term(POS, TermType.INT, 0)
                ),
                WhileStatement(
                    POS,
                    LessThanExpression(
                        POS,
                        Identifier(POS, 'i'),
                        Term(POS, TermType.INT, 3)
                    ),
                    OperationBlock(
                        POS,
                        [
                            Assignment(
                                POS,
                                Identifier(POS, 'a'),
                                AdditionExpression(
                                    POS,
                                    Identifier(POS, 'a'),
                                    Identifier(POS, 'i')
                                )
                            ),
                            BreakStatement(POS),
                        ]
                    ),
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 0

    def test_return_statement(self):
        program = Program(
            POS,
            [
                FunctionDefinition(
                    POS,
                    'f',
                    [],
                    OperationBlock(
                        POS,
                        [
                            ReturnStatement(
                                POS,
                                Term(POS, TermType.INT, 1)
                            )
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    FunCall(
                        POS,
                        'f',
                        []
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('a').get_value() == 1

    def test_dot_access(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    FunCall(
                        POS,
                        'Point',
                        [
                            Term(POS, TermType.INT, 1),
                            Term(POS, TermType.INT, 2),
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    DotAccess(
                        POS,
                        Identifier(POS, 'a'),
                        [Identifier(POS, 'y')]
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('b').get_value() == 2

    def test_function_call(self):
        program = Program(
            POS,
            [
                FunctionDefinition(
                    POS,
                    'f',
                    [Parameter(POS, 'a')],
                    OperationBlock(
                        POS,
                        [
                            ReturnStatement(
                                POS,
                                Identifier(POS, 'a')
                            )
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    FunCall(
                        POS,
                        'f',
                        [Term(POS, TermType.INT, 1)]
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('b').get_value() == 1

    def test_function_call_with_scope(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                FunctionDefinition(
                    POS,
                    'f',
                    [Parameter(POS, 'a')],
                    OperationBlock(
                        POS,
                        [
                            ReturnStatement(
                                POS,
                                Identifier(POS, 'a')
                            )
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    FunCall(
                        POS,
                        'f',
                        [Term(POS, TermType.INT, 2)]
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('b').get_value() == 2

    def test_function_call_with_scope_and_new_scope(self):
        program = Program(
            POS,
            [
                VariableAssignment(
                    POS,
                    Identifier(POS, 'a'),
                    Term(POS, TermType.INT, 1)
                ),
                FunctionDefinition(
                    POS,
                    'f',
                    [Parameter(POS, 'a')],
                    OperationBlock(
                        POS,
                        [
                            VariableAssignment(
                                POS,
                                Identifier(POS, 'a'),
                                Term(POS, TermType.INT, 2)
                            ),
                            ReturnStatement(
                                POS,
                                Identifier(POS, 'a')
                            )
                        ]
                    )
                ),
                VariableAssignment(
                    POS,
                    Identifier(POS, 'b'),
                    FunCall(
                        POS,
                        'f',
                        [Term(POS, TermType.INT, 3)]
                    )
                ),
            ]
        )
        interpreter = Interpreter(MAXIMUM_RECURSION_DEPTH)
        interpreter.interpret(program)
        assert interpreter.current_scope().get('b').get_value() == 2
        assert interpreter.current_scope().get('a').get_value() == 1
