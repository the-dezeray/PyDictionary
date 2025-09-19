from renderers.abtract_render import Renderer
from components.layouts import settings_layout,menu_layout
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from components.settings import getTable
class MenuRenderer(Renderer):
    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "MenuLayout"
    def update(self,core)->Layout:
        layout = menu_layout()
        panel = Panel(getTable(self.core), title="[bold blue]Main Menu[/bold blue]",title_align="left",  border_style="bright_blue")
        layout["main"].update(Align.center(panel, vertical="middle"))
        return layout
