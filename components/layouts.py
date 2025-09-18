from rich.layout import Layout
from rich.padding import Padding
from rich.console import Console,Group
from rich.spinner import Spinner
from components.settings import getTable
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

    )
    
    layout["header"].update(Padding(pad=(0,70),renderable=Spinner(name="dots12")))
    
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