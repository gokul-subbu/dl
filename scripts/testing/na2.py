class na2:
    def hello():
        print("inside the instance block no args")

    def inst_hello(args):
        print(f'instance hello from {args}')

    @classmethod
    def class_hello(args):
        print(f"hello from {args}")
    

