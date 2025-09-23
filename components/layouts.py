from rich.layout import Layout
from rich.padding import Padding
from rich.console import Console,Group
from rich.spinner import Spinner
from components.settings import getTable
from rich.align import Align
def main_layout()->Layout:
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
  
        Layout(name="footer",size=1)

    )
    



    layout["header"].update(Align.center(renderable=Spinner(name="earth")))
    
    layout["footer"].split_row(
        Layout(name="footer_left"),

        Layout(name="footer_right")
    )
    layout["footer_left"].update(Align.left(renderable="pyDictionary v0.1.0"))
    layout["footer_right"].update(Align.right(renderable="menu: [bold cyan]TAB[/bold cyan] | exit: [red1]ESC[/red1]  "))
    return layout
def settings_layout()->Layout:
    """return a structured Layout object for settings

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="main") 

    

    return layout

def menu_layout()->Layout:
    """return a structured Layout object for settings

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="main") 

    return layout