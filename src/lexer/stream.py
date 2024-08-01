class Stream:
    def __init__(self, stream):
        self.stream = stream
        self.current_char = None
        self.current_position = TextPosition(1, 0)

        self.next_char()

    def next_char(self):
        char = self.stream.read(1)
        if not char:
            self.current_char = 'EOF'
            self.current_position.next_column()
        elif char == '\n':
            self.current_char = '\n'
            self.current_position.next_line()
            self.current_position.current_column = 0
        else:
            self.current_char = char
            self.current_position.next_column()
        return self.current_char

    def get_char(self):
        return self.current_char

    def get_position(self):
        return self.current_position


class TextPosition:
    def __init__(self, line, column):
        self.current_line = line
        self.current_column = column

    def __str__(self):
        return f'|ln: {self.current_line:<4}|col: {self.current_column:<4}| '

    def next_line(self):
        self.current_line += 1

    def next_column(self):
        self.current_column += 1
