class hi_me:
    def __init__(self):
        self.x=1
        print('initializing')

    def __call__(self, y):
        print(self.x)
        self.x+=y


brrr=hi_me()

