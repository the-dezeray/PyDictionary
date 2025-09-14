"""handles program launch"""
import queue
import time

from pynput.keyboard  import Listener
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.padding import Padding
from rich.console import Console,Group
from rich.spinner import Spinner

from art import text2art

from core import Core
from dependecies import check_dependecies, install_dependecies
console = Console()

def l2():
    """return a structured Layout object

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(

        Layout(name="main"),

    )
    
    
    return layout
def lll():
    """return a structured Layout object

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(
        Layout(name = "header",size =2),
        Layout(name="main", size = 3),
        Layout(name = "suggestion",size=3),
        
        Layout(name = "view",ratio=4),

    )
    
    layout["header"].update(Padding(pad=(0,70),renderable=Spinner(name="dots12")))
    
    return layout
class CustomLayout:
    def __init__(self,core):
        self.core = core
        self.name = "CustomLayout"
        ...
    def update(self):
        layout = lll()
class DictionaryLayout(CustomLayout):

    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "DictionaryLayout"
        self.f = 0
        

    def update(self):
        core : Core = self.core
        core.layout = lll()
        if self.f == 0:
            self.f = 1 
            (word,meaning) = self.core.get_word_of_the_day()
            art = text2art(f"{word}",font="tarty4")
            from rich.align import Align
            core.layout["view"].update(Padding(pad=(0,10),renderable=Padding(Align(f"[green]{art}[/green] \n\n{meaning}",align="center"))))
        else:
            core.layout["view"].update(Padding(core.table,pad =(0,40),expand=True))
        core.layout["main"].update(Padding(Panel(core.formated_entry_text),pad =(0,20)))
        core.layout["suggestion"].update(Padding(core.suggestion,pad =(0,20),expand=True))
        return core.layout
    
class SettingTab(CustomLayout):

    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "SettingTab"

    def update(self):
        core : Core = self.core
        core.layout = l2()
        core.table = core.getTable();
        core.layout["main"].update(Padding(core.table,expand=True))

        return core.layout
        
     
def menu_layout():
    """return a structured Layout object for menu

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(
        Layout(name = "header"),
        Layout(name="main", ),

    )
    
    layout["header"].update(Padding(pad=(0,70),renderable=Spinner(name="dots12")))
    
    return layout