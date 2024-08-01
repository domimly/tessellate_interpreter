class LexerError(Exception):
    def __str__(self):
        return f'\n\nLexer error: {self.message} {self.position}'


class InvalidSyntaxError(LexerError):
    def __init__(self, position):
        self.message = 'Invalid syntax -- forbidden character'
        self.position = position


class IdentifierTooLongError(LexerError):
    def __init__(self, max_id, position):
        self.message = (
            'ID longer than maximum ' +
            f'({max_id} characters)'
        )
        self.position = position


class StringTooLongError(LexerError):
    def __init__(self, max_string, position):
        self.message = (
            'String longer than maximum ' +
            f'({max_string} characters)'
        )
        self.position = position


class InvalidEscapeSequenceError(LexerError):
    def __init__(self, char, position):
        self.message = f'Attempt to escape an unfitting character: \\{char}'
        self.position = position


class UnclosedStringError(LexerError):
    def __init__(self, position):
        self.message = 'Unclosed string'
        self.position = position


class IntTooBigError(LexerError):
    def __init__(self, max_int, position):
        self.message = (
            f'Integer bigger than maximum ({max_int})'
        )
        self.position = position


class TooManyDecimalsInFloatError(LexerError):
    def __init__(self, max_float_decimals, position):
        self.message = (
            'Too many digits after a decimal in float ' +
            f'(maximum {max_float_decimals} digits)'
        )
        self.position = position
