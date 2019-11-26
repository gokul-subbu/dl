class student:
    def __init__(self, name:str, roll:int, sec:str):
        self.name=name
        self.roll=roll
        self.sec=sec

    def __repr__(self):
        return f'{self.name}, {self.roll}'

    def __str__(self):
        return f'{self.name} {self.roll} {self.sec}'

pachi=student('pachi', 44, 'c')

narain=student('narain', 33, 'a')

print(pachi)
print(narain)
