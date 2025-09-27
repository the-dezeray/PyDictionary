from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..core import Core
    from rich.layout import Layout
class Renderer(ABC):
    def __init__(self,core):
        self.core = core
        self.name = "CustomLayout"
        ...
    @abstractmethod
    def update(self,ui_state:"Core")-> "Layout":
        ...