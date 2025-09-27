from abc import ABC, abstractmethod
class Renderer(ABC):
    def __init__(self,core):
        self.core = core
        self.name = "CustomLayout"
        ...
    @abstractmethod
    def update(self):
        ...