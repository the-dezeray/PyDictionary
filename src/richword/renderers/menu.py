from .abtract_render import Renderer
from ..components.layouts import settings_layout,menu_layout
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from ..components.settings import getTable
class MenuRenderer(Renderer):
    def __init__(self,ui_state):
        super().__init__(ui_state)
        self.ui_state = ui_state
        self.name = "MenuLayout"
    def update(self,ui_state)->Layout:
        layout = menu_layout()
        panel = Panel(getTable(self.ui_state), title="[bold blue]Main Menu[/bold blue]",title_align="left",  border_style="bright_blue")
        layout["main"].update(Align.center(panel, vertical="middle"))
        return layout
