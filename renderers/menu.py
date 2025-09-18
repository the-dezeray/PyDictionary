from renderers.abtract_render import Renderer
from components.layouts import settings_layout,menu_layout
from rich.layout import Layout
from components.settings import getTable
class MenuRenderer(Renderer):
    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "MenuLayout"
    def update(self,core)->Layout:
        layout = menu_layout()
        layout["main"].update(getTable(self.core))
        return layout
