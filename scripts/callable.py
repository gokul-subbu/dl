class MyClass:
    def __init__(self):
        print('initializing...')
        self.counter=0

    def __call__(self, x=1):
        self.counter +=x
        print(self.counter)


m=MyClass()
