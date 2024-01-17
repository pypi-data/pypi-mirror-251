from abc import ABC, abstractmethod


class FileParser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getData(self, filePath):
        pass
