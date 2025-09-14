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


from customLayouts import DictionaryLayout
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