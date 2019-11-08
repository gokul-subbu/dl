import abc

class Driveable(abc.ABC):
    @abc.abstractmethod
    def drive(self):
        pass

class Car(Driveable):
    def drive(self):
        print("driving")
