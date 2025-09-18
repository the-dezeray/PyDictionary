from renderers.abtract_render import Renderer
from components.layouts import settings_layout,menu_layout
from rich.layout import Layout
from rich.panel import Panel
from components.settings import getTable
class QuizGameRenderer(Renderer):
    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "MenuLayout"
    def update(self,core)->Layout:
        layout = menu_layout()
        from rich.console import Group
        from rich.align import Align
        from rich.padding import Padding
        from art import text2art
     
        word = Align(renderable= Padding("ted"),align="center", pad=(0, 20))
        renderable = Group(word,Panel("hios"))
        layout["main"].update(renderable=renderable)
        return layout
