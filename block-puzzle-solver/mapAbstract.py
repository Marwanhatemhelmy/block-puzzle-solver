from abc import ABC, abstractmethod

class MapAbstractMethods(ABC):
    @abstractmethod
    def blastMap(self):
        pass

    @abstractmethod
    def returnNumberOfFreeSlots(self):
        pass