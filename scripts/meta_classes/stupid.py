def stupid_metaclass(classname, bases, attrdict):
    return type(classname, bases, attrdict)

class Myclass(metaclass=stupid_metaclass):
    pass
