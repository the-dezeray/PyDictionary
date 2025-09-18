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
from input_handler import InputHandler


from core import Core

from ui_manager import UIManager
console = Console()
from app_state import AppState,UIState

from renderers.dictionary import DictionaryRenderer
def main():
    """Program Launch"""

    core = Core()
    appState = AppState.DICTIONARY
    uiState = UIState(current_screen=appState)
    #core.layout = DictionaryRenderer(core=core)
    ui_manager = UIManager(core=core)
    
    ui_manager.live = Live(ui_manager.get_current_layout(), refresh_per_second=10,auto_refresh=True)
    core.ui_manager = ui_manager
    input_handler =InputHandler(core=core, ui_manager=ui_manager)
    keyboard_listener  = Listener(on_press= input_handler.handle_key)
    #listens for keyboard key press
    with keyboard_listener as l :
        #Renders an auto-updating terminal
        with ui_manager.live:
            while core.running: #if program has not been terminated
                ...

        keyboard_listener.join()

if __name__ == "__main__":
 
    main()