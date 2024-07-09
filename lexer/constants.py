MAXIMUM_IDENTIFIER = 80
MAXIMUM_STRING = 1000
MAXIMUM_INT_DIGITS = 32

INVALID_SYNTAX_ERROR_MSG = 'Invalid syntax - forbidden character'

IDENTIFIER_TOO_LONG_ERROR_MSG = (
    'ID longer than maximum ' +
    f'({MAXIMUM_IDENTIFIER} characters)'
)

STRING_TOO_LONG_ERROR_MSG = (
    'String longer than maximum ' +
    f'({MAXIMUM_STRING} characters)'
)

UNCLOSED_STRING_ERROR_MSG = 'Unclosed string'

INT_TOO_BIG_ERROR_MSG = (
    'Integer longer than maximum ' +
    f'({MAXIMUM_INT_DIGITS} digits)'
)
