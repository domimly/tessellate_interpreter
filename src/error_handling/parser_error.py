class ParserError(Exception):
    def __str__(self):
        return f'\n\nParser error: {self.message} {self.position}'


class UnexpectedTokenError(ParserError):
    def __init__(self, position, token_type, token_found):
        self.message = (
            f'Unexpected token -- expected: {token_type}, ' +
            f'found: {token_found.token_type}'
        )
        self.position = position


class InvalidSyntaxError(ParserError):
    def __init__(self, position, msg):
        self.message = f'Invalid syntax -- {msg}'
        self.position = position
