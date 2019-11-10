class AnswerType(type):
    def __init__(self, name, bases, namespaces):
        self.answer=42


class book(metaclass=AnswerType):
    pass

print(book.answer)
