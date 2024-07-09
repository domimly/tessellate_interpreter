class LexerError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position

    def __str__(self):
        return f'Lexer error: {self.message} {self.position}'
