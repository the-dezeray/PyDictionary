"""handles program launch"""
import time
from pynput.keyboard  import Listener
from rich.live import Live
from rich.console import Console
from .input_handler import InputHandler
from .core import Core
from .ui_manager import UIManager

console = Console()

def main():
    """Program Launch"""

    ui_state = Core()
    #core.layout = DictionaryRenderer(core=core)
    ui_manager = UIManager(ui_state=ui_state)

    ui_manager.live = Live(ui_manager.get_current_layout(), refresh_per_second=10,auto_refresh=True,screen=True)
    ui_state.ui_manager = ui_manager
    input_handler =InputHandler(ui_state=ui_state, ui_manager=ui_manager)
    keyboard_listener  = Listener(on_press= input_handler.handle_key)
    #listens for keyboard key press

    with keyboard_listener as l :
        #Renders an auto-updating terminal
        with ui_manager.live:
            while ui_state.running: #if program has not been terminated
                time.sleep(0.4)
        keyboard_listener.stop()
        ui_manager.live.stop()   
        keyboard_listener.join()

if __name__ == "__main__":
 
    main()