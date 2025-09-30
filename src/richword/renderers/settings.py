from .abtract_render import Renderer
from ..components.layouts import settings_layout
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rich.layout import Layout
    from  ..ui_state import UiState
class SettingsRenderer(Renderer):
    def __init__(self,ui_state:"UiState"):
        super().__init__(ui_state)
        self.ui_state = ui_state
        self.name = "SettingsLayout"
    def update(self,ui_state:"UiState")->"Layout":
        layout = settings_layout()
        return layout
        