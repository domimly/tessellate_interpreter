from enum import Enum, auto


class TokenType(Enum):
    # characters
    SEMICOLON = auto()              # ;
    COMMA = auto()                  # ,
    POINT = auto()                  # .
    LEFT_PARENTHASIS = auto()       # (
    RIGHT_PARENTHASIS = auto()      # )
    LEFT_CURLY_BRACKETS = auto()    # {
    RIGHT_CURLY_BRACKETS = auto()   # }
    LEFT_SQUARE_BRACKETS = auto()   # [
    RIGHT_SQUARE_BRACKETS = auto()  # ]

    # operators
    ASSIGN_OPERATOR = auto()            # =
    ADD_OPERATOR = auto()               # +
    SUBTRACT_OPERATOR = auto()          # -
    MULTIPLY_OPERATOR = auto()          # *
    DIVIDE_OPERATOR = auto()            # /
    FLOOR_DIVIDE_OPERATOR = auto()      # //
    MODULO_OPERATOR = auto()            # %
    POWER_OPERATOR = auto()             # **
    AND_OPERATOR = auto()               # &&
    OR_OPERATOR = auto()                # ||
    EQUAL_OPERATOR = auto()             # ==
    NOT_EQUAL_OPERATOR = auto()         # !=
    LESS_THAN_OPERATOR = auto()         # <
    LESS_OR_EQUAL_OPERATOR = auto()     # <=
    MORE_THAN_OPERATOR = auto()         # >
    MORE_OR_EQUAL_OPERATOR = auto()     # >=
    NEGATION_OPERATOR = auto()          # !

    # data types
    INTEGER = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()

    # keywords
    DEF = auto()
    VAR = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    WHILE = auto()
    BREAK = auto()
    RETURN = auto()

    # other
    IDENTIFIER = auto()
    END_OF_FILE = auto()


class Token:
    def __init__(self, token_type, position, value=None):
        self.token_type = token_type
        self.position = position
        self.value = value

    def __str__(self):
        token_repr = (
            f'type: {self.token_type.name:<25}'
            f'pos: {self.position}'
        )
        if self.value:
            token_repr += f'value: {self.value}'
        return token_repr
