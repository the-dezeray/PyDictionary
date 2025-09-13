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



from core import Core
from dependecies import check_dependecies, install_dependecies
console = Console()

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
        ...
    def update(self):
        layout = lll()
class DictionaryLayout(CustomLayout):

    def __init__(self,core):
        super().__init__(core)
        self.core = core
        

    def update(self):
        core : Core = self.core
        core.layout = lll()

        core.layout["view"].update(Padding(core.table,pad =(0,40),expand=True))
        core.layout["main"].update(Padding(Panel(core.formated_entry_text),pad =(0,20)))
        core.layout["suggestion"].update(Padding(core.suggestion,pad =(0,20),expand=True))
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

def main():
    """Program Launch"""

    core = Core()
    core.clayout = DictionaryLayout(core=core)
    #listens for keyboard key press
    with Listener(on_press= core.save_key) as L:
        #Renders an auto-updating terminal
        with Live(core.clayout.update(), refresh_per_second=10,auto_refresh=True) as core.live:  # update 10  times a second to feel fluid

            while core.running: #if program has not been terminated
                ...

        L.join()
    
                
if __name__ == "__main__":
    if not check_dependecies() : install_dependecies 
    main()