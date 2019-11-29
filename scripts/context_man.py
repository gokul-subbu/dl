class MyContext:
    def __init__(self):
        self.obj=None

    def __enter__(self):
        print('entering context...')
        self.obj='the return object'
        return self.obj

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context...')
        if exc_type:
            print(f'*** error occured: {exc_type}, {exc_value}')
        return True

class Resource:
    def __init__(self, name):
        self.name=name
        self.state=None


class ResourceManager:
    def __init__(self, name):
        self.name=name
        self.resource=None

    def __enter__(self):
        print('entering context')
        self.resource=Resource(self.name)
        self.resource.state='created'
        return self.resource

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context')
        self.resource.state='destroyed'
        if exc_type:
            print('error occured')
        return False



