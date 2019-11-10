class AnswerType(type):
    def __init__(self, name, bases, namespace):
        self.answer=42


class Book(metaclass=AnswerType): pass

assert Book.answer==42
