from src.lexer.tokens import TokenType
from src.error_handling.parser_error import (
    UnexpectedTokenError, InvalidSyntaxError
)
from src.parser.parser_tree import (
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
    ListIndex,
    TermType
)

listable = [
    TokenType.IDENTIFIER,
    TokenType.INTEGER,
    TokenType.FLOAT,
    TokenType.BOOL,
    TokenType.STRING,
    TokenType.LEFT_PARENTHASIS,
    TokenType.LEFT_SQUARE_BRACKETS,
]


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.tokenize()

    def consume_token(self):
        self.token = self.lexer.tokenize()

    def token_must_be(self, token_type):
        if self.token.token_type != token_type:
            raise UnexpectedTokenError(
                self.get_position(),
                token_type,
                self.token
            )
        value = self.token.value
        self.consume_token()
        return value

    def get_position(self):
        return [
            self.lexer.current_token_position.current_line,
            self.lexer.current_token_position.current_column
        ]

    # program ::= {statement};
    def parse_program(self):
        statements = []
        while (stmt := self.parse_statement()):
            statements.append(stmt)
        self.token_must_be(TokenType.END_OF_FILE)
        return Program([0, 0], statements)

    # statement ::= block_statement | function_definition;
    def parse_statement(self):
        if stmt := self.parse_function_definition():
            return stmt
        if stmt := self.parse_block_statement():
            return stmt
        return None

    # block_statement         ::= assignment_statement_or_call
    #                             | break_statement
    #                             | return_statement
    #                             | if_statement
    #                             | while_statement
    #                             | for_statement;
    #                             | expression;
    def parse_block_statement(self):
        if stmt := self.parse_break_statement():
            return stmt
        if stmt := self.parse_return_statement():
            return stmt
        if stmt := self.parse_assignment_or_call():
            return stmt
        if stmt := self.parse_if_statement():
            return stmt
        if stmt := self.parse_while_statement():
            return stmt
        if stmt := self.parse_for_statement():
            return stmt
        if stmt := self.parse_expression():
            return stmt
        return None

    # break_statement ::= 'break', ';';
    def parse_break_statement(self):
        if self.token.token_type != TokenType.BREAK:
            return None
        pos = self.get_position()
        self.consume_token()
        self.token_must_be(TokenType.SEMICOLON)
        return BreakStatement(pos)

    # return_statement ::= 'return', [expression], ';';
    def parse_return_statement(self):
        if self.token.token_type != TokenType.RETURN:
            return None
        pos = self.get_position()
        self.consume_token()
        value = self.parse_expression()
        self.token_must_be(TokenType.SEMICOLON)
        return ReturnStatement(pos, value)

    # assignment_statement_or_call ::= call, ["=", expression], ';';
    def parse_assignment_or_call(self):
        if self.token.token_type != TokenType.IDENTIFIER:
            return None
        pos = self.get_position()
        call = self.parse_call()
        if self.token.token_type == TokenType.SEMICOLON:
            self.consume_token()
            return call
        self.token_must_be(TokenType.ASSIGN_OPERATOR)
        if self.token.token_type == TokenType.LEFT_SQUARE_BRACKETS:
            value = self.parse_list()
        else:
            value = self.parse_expression()
        if not value:
            raise InvalidSyntaxError(
                pos,
                'No value after ASSIGN operator in assignment'
            )
        self.token_must_be(TokenType.SEMICOLON)
        return Assignment(pos, call, value)

    # list ::= "[", [expression, {",", expression}], "]";
    def parse_list(self):
        if self.token.token_type != TokenType.LEFT_SQUARE_BRACKETS:
            return None
        pos = self.get_position()
        self.consume_token()
        values = []
        values.append(self.parse_expression())
        while self.token.token_type == TokenType.COMMA:
            self.consume_token()
            if value := self.parse_expression():
                values.append(value)
            else:
                raise InvalidSyntaxError(
                    pos,
                    'No value after COMMA operator in list creation'
                )
        self.token_must_be(TokenType.RIGHT_SQUARE_BRACKETS)
        return List(pos, values)

    # list_index ::= "[", int, "]";
    def parse_list_index(self):
        if self.token.token_type != TokenType.LEFT_SQUARE_BRACKETS:
            return None
        pos = self.get_position()
        self.consume_token()
        index = self.token_must_be(TokenType.INTEGER)
        self.token_must_be(TokenType.RIGHT_SQUARE_BRACKETS)
        return ListIndex(pos, index)

    # single_call ::= identifier, [argument_list | list_index];
    # argument_list ::= "(", [expression, {",", expression}], ")";
    def parse_single_call(self):
        if self.token.token_type != TokenType.IDENTIFIER:
            return None
        identifier = self.token.value
        pos = self.get_position()
        self.consume_token()
        arguments = []
        list_index = None
        if self.token.token_type == TokenType.LEFT_PARENTHASIS:
            self.consume_token()
            while arg := self.parse_expression():
                arguments.append(arg)
                if self.token.token_type == TokenType.COMMA:
                    self.consume_token()
                else:
                    break
            self.token_must_be(TokenType.RIGHT_PARENTHASIS)
        elif self.token.token_type == TokenType.LEFT_SQUARE_BRACKETS:
            list_index = self.parse_list_index()
        return SingleCall(pos, identifier, arguments, list_index)

    # call ::= call, ".", {call};
    def parse_call(self):
        if self.token.token_type != TokenType.IDENTIFIER:
            return None
        pos = self.get_position()
        calls = []
        calls.append(self.parse_single_call())
        while self.token.token_type == TokenType.POINT:
            self.consume_token()
            if call := self.parse_single_call():
                calls.append(call)
            else:
                raise InvalidSyntaxError(
                    pos,
                    'No call after POINT operator'
                )
        return Call(pos, calls)

    # if_statement ::= "if", "(", expression, ")", operation_block,
    #                 ["else", operation_block];
    def parse_if_statement(self):
        if self.token.token_type != TokenType.IF:
            return None
        pos = self.get_position()
        self.consume_token()
        self.token_must_be(TokenType.LEFT_PARENTHASIS)
        condition = self.parse_expression()
        self.token_must_be(TokenType.RIGHT_PARENTHASIS)
        if_block = self.parse_operation_block()
        else_block = None
        if self.token.token_type == TokenType.ELSE:
            self.consume_token()
            else_block = self.parse_operation_block()
        return IfStatement(pos, condition, if_block, else_block)

    # while_statement ::= "while", "(", expression, ")", operation_block;
    def parse_while_statement(self):
        if self.token.token_type != TokenType.WHILE:
            return None
        pos = self.get_position()
        self.consume_token()
        self.token_must_be(TokenType.LEFT_PARENTHASIS)
        condition = self.parse_expression()
        self.token_must_be(TokenType.RIGHT_PARENTHASIS)
        operation = self.parse_operation_block()
        return WhileStatement(pos, condition, operation)

    # for_statement ::= "for", "(", identifier, "in", call | list, ")",
    #                   operation_block;
    def parse_for_statement(self):
        if self.token.token_type != TokenType.FOR:
            return None
        pos = self.get_position()
        self.consume_token()
        self.token_must_be(TokenType.LEFT_PARENTHASIS)
        identifier = self.token_must_be(TokenType.IDENTIFIER)
        self.token_must_be(TokenType.IN)
        iterable = self.parse_list() or self.parse_expression()
        self.token_must_be(TokenType.RIGHT_PARENTHASIS)
        operation = self.parse_operation_block()
        return ForStatement(pos, identifier, iterable, operation)

    # "def", identifier, parameter_list, operation_block;
    def parse_function_definition(self):
        if self.token.token_type != TokenType.DEF:
            return None
        pos = self.get_position()
        self.consume_token()
        identifier = self.token_must_be(TokenType.IDENTIFIER)
        parameters = self.parse_parameter_list()
        operation_block = self.parse_operation_block()
        return FunctionDefinition(
            pos, identifier,
            parameters,
            operation_block
        )

    # parameter_list ::= "(", [identifier, {",", identifier}], ")";
    def parse_parameter_list(self):
        self.token_must_be(TokenType.LEFT_PARENTHASIS)
        parameters = []
        if self.token.token_type != TokenType.IDENTIFIER:
            self.token_must_be(TokenType.RIGHT_PARENTHASIS)
            return parameters
        pos = self.get_position()
        parameters.append(Parameter(pos, self.token.value))
        self.consume_token()
        while self.token.token_type == TokenType.COMMA:
            self.consume_token()
            pos = self.get_position()
            value = self.token_must_be(TokenType.IDENTIFIER)
            parameters.append(Parameter(pos, value))
        self.token_must_be(TokenType.RIGHT_PARENTHASIS)
        return parameters

    # operation_block ::= "{", {block_statement}, "}";
    def parse_operation_block(self):
        pos = self.get_position()
        self.token_must_be(TokenType.LEFT_CURLY_BRACKETS)
        operations = []
        while operation := self.parse_block_statement():
            operations.append(operation)
        self.token_must_be(TokenType.RIGHT_CURLY_BRACKETS)
        return OperationBlock(pos, operations)

    # expression ::= and_expression, {or_operator, and_expression};
    def parse_expression(self):
        left_factor = self.parse_and_expression()
        if not left_factor:
            return None
        while self.token.token_type == TokenType.OR_OPERATOR:
            pos = self.get_position()
            self.consume_token()
            right_factor = self.parse_and_expression()
            if not right_factor:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for OR expression'
                )
            left_factor = OrExpression(
                pos,
                left_factor,
                right_factor
            )
        return left_factor

    # and_expression ::=
    # relation_expression, {and_operator, relation_expression};
    def parse_and_expression(self):
        left_factor = self.parse_relation_expression()
        if not left_factor:
            return None
        while self.token.token_type == TokenType.AND_OPERATOR:
            pos = self.get_position()
            self.consume_token()
            right_factor = self.parse_relation_expression()
            if not right_factor:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for AND expression'
                )
            left_factor = AndExpression(
                pos,
                left_factor,
                right_factor
            )
        return left_factor

    # relation_expression ::=
    # add_expression, [ relation_operator, add_expression ];
    def parse_relation_expression(self):
        left = self.parse_add_expression()
        if not left:
            return None
        if self.token.token_type in (
            TokenType.LESS_THAN_OPERATOR,
            TokenType.MORE_THAN_OPERATOR,
            TokenType.LESS_OR_EQUAL_OPERATOR,
            TokenType.MORE_OR_EQUAL_OPERATOR,
            TokenType.EQUAL_OPERATOR,
            TokenType.NOT_EQUAL_OPERATOR
        ):
            pos = self.get_position()
            operator = self.token
            self.consume_token()
            right = self.parse_add_expression()
            if not right:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for relation expression'
                )
            if operator.token_type == TokenType.LESS_THAN_OPERATOR:
                return LessThanExpression(pos, left, right)
            if operator.token_type == TokenType.MORE_THAN_OPERATOR:
                return GreaterThanExpression(pos, left, right)
            if operator.token_type == TokenType.LESS_OR_EQUAL_OPERATOR:
                return LessOrEqualExpression(pos, left, right)
            if operator.token_type == TokenType.MORE_OR_EQUAL_OPERATOR:
                return GreaterOrEqualExpression(pos, left, right)
            if operator.token_type == TokenType.EQUAL_OPERATOR:
                return EqualityExpression(pos, left, right)
            if operator.token_type == TokenType.NOT_EQUAL_OPERATOR:
                return InequalityExpression(pos, left, right)
        return left

    # add_expression
    # ::= multiply_expression, { add_operator, multiply_expression };
    def parse_add_expression(self):
        left = self.parse_multiply_expression()
        if not left:
            return None
        while self.token.token_type in (
            TokenType.ADD_OPERATOR,
            TokenType.SUBTRACT_OPERATOR
        ):
            pos = self.get_position()
            operator = self.token
            self.consume_token()
            right = self.parse_multiply_expression()
            if not right:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for addition/subtraction expression'
                )
            if operator.token_type == TokenType.ADD_OPERATOR:
                left = AdditionExpression(pos, left, right)
            else:
                left = SubtractionExpression(pos, left, right)
        return left

    # multiply_expression
    # ::= power_expression, { multiply_operator, power_expression};
    def parse_multiply_expression(self):
        left = self.parse_power_expression()
        if not left:
            return None
        while self.token.token_type in (
            TokenType.MULTIPLY_OPERATOR,
            TokenType.DIVIDE_OPERATOR,
        ):
            pos = self.get_position()
            operator = self.token
            self.consume_token()
            right = self.parse_power_expression()
            if not right:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for multiplication/division expression'
                )
            if operator.token_type == TokenType.MULTIPLY_OPERATOR:
                left = MultiplicationExpression(pos, left, right)
            else:
                left = DivisionExpression(pos, left, right)
        return left

    # power_expression ::= not_expression, { "**", not_expression};
    def parse_power_expression(self):
        left = self.parse_not_expression()
        if not left:
            return None
        while self.token.token_type == TokenType.POWER_OPERATOR:
            pos = self.get_position()
            self.consume_token()
            right = self.parse_not_expression()
            if not right:
                raise InvalidSyntaxError(
                    pos,
                    'No right factor for power expression'
                )
            left = PowerExpression(pos, left, right)
        return left

    # not_expression ::= [not_operator], term;
    def parse_not_expression(self):
        if self.token.token_type in [
            TokenType.NEGATION_OPERATOR, TokenType.SUBTRACT_OPERATOR
        ]:
            pos = self.get_position()
            self.consume_token()
            term = self.parse_term()
            if not term:
                raise InvalidSyntaxError(
                    pos,
                    'No factor for NOT expression'
                )
            return NotExpression(pos, term)
        return self.parse_term()

    # term                        ::= int
    #                                 | float
    #                                 | bool
    #                                 | string
    #                                 | call
    #                                 | '(' expression ')';
    def parse_term(self):
        pos = self.get_position()
        if (self.token.token_type == TokenType.INTEGER):
            value = self.token.value
            self.consume_token()
            return Term(pos, TermType.INT, value)
        if (self.token.token_type == TokenType.FLOAT):
            value = self.token.value
            self.consume_token()
            return Term(pos, TermType.FLOAT, value)
        if (self.token.token_type == TokenType.BOOL):
            value = self.token.value
            self.consume_token()
            return Term(pos, TermType.BOOL, value)
        if (self.token.token_type == TokenType.STRING):
            value = self.token.value
            self.consume_token()
            return Term(pos, TermType.STRING, value)
        if self.token.token_type == TokenType.IDENTIFIER:
            return self.parse_call()
        if self.token.token_type == TokenType.LEFT_PARENTHASIS:
            self.consume_token()
            expr = self.parse_expression()
            self.token_must_be(TokenType.RIGHT_PARENTHASIS)
            return expr
        return None
