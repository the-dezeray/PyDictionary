from .abtract_render import Renderer
from ..components.layouts import settings_layout
class SettingsRenderer(Renderer):
    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "SettingsLayout"
    def update(self,core):
        layout = settings_layout()
        