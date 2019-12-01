class Rectange:
    def __init__(self, width, height):
        self.width=width
        self.height=height

    def area(self): return self.height*self.width

    def perimeter(self): return 2*(self.width+self.height)

    def __str__(self): return f'Rectangle ({self.height}, self.width)'

    def __repr__(self): return f'Rectangle ({self.height}, {self.width})'

    def __eq__(self, other: Rectangle):
        return self.area==other.area

    def __lt__(self, other: Rectangle): return self.area()<other.area()

    # def __gt__(self, other: Rectangle): return self.area()>other.area()


