from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..ui_state import UiState
    from rich.layout import Layout
class Renderer(ABC):
    def __init__(self,core):
        self.core = core
        self.name = "CustomLayout"
        ...
    @abstractmethod
    def update(self,ui_state:"UiState")-> "Layout":
        ...