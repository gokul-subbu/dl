class entry_exit():
    def __init__(self, f):
        self.f = f

    def __call__(self):
        print("entering", self.f.__name__)
        self.f()
        print("excited", self.f.__name__)


@entry_exit
def func1():
    print("inside func1()")


@entry_exit
def func2():
    print("inside func2()")

func1()
func2()
