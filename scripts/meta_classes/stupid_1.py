class MyMeta(type):
    pass

class MyClass(metaclass=MyMeta):
    pass

inst=MyClass()
