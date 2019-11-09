class MultiBases(type):
    def __new__(cls, clsname, bases, clsdict):
        if len(bases)>1:
            raise TypeError("Inherited multiple base classes")
        return super().__new__(cls, clsname, bases, clsdict)


class Base(metaclass=MultiBases):
    pass

class A(Base):
    pass

class B(Base):
    pass

class C(A, B):
    pass
