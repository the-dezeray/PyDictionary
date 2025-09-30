"""handles program launch"""
import time
from pynput.keyboard  import Listener
from rich.live import Live
from rich.console import Console
from .input_handler import InputHandler
from .ui_state import UiState
from .ui_manager import UIManager
from .util.nltk_handler import first_init

console = Console()

def main():
    """Program Launch"""
    
    # Initialize NLTK and WordNet data in a separate thread
    print("Starting NLTK initialization...")
    init_thread = first_init()

    ui_state = UiState()
    #core.layout = DictionaryRenderer(core=core)
    ui_manager = UIManager(ui_state=ui_state)

    ui_manager.live = Live(ui_manager.get_current_layout(), refresh_per_second=10,auto_refresh=True,screen=True)
    ui_state.ui_manager = ui_manager
    input_handler =InputHandler(ui_state=ui_state, ui_manager=ui_manager)
    keyboard_listener  = Listener(on_press= input_handler.handle_key)
    #listens for keyboard key press

    with keyboard_listener:
        #Renders an auto-updating terminal
        with ui_manager.live:
            while ui_state.running: #if program has not been terminated
                time.sleep(0.4)
        keyboard_listener.stop()
        ui_manager.live.stop()   
        keyboard_listener.join()
    
    # Wait for NLTK initialization thread to complete (if still running)
    if init_thread.is_alive():
        init_thread.join(timeout=5.0)

if __name__ == "__main__":
 
    main()