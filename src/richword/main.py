"""handles program launch"""
import time
from pynput.keyboard  import Listener
from rich.live import Live
from rich.console import Console
from .input_handler import InputHandler
from .ui_state import UiState
from .ui_manager import UIManager
from .util.nltk_handler import first_init
from .util.logger import get_logger

console = Console()
logger = get_logger(__name__)

def main():
    """Program Launch"""
    logger.info("Starting RichWord application")
    
    try:
        # Initialize NLTK and WordNet data in a separate thread
        logger.info("Starting NLTK initialization...")
        print("Starting NLTK initialization...")
        init_thread = first_init()

        logger.debug("Creating UI state and manager")
        ui_state = UiState()
        #core.layout = DictionaryRenderer(core=core)
        ui_manager = UIManager(ui_state=ui_state)

        logger.debug("Setting up Live display with 10fps refresh rate")
        ui_manager.live = Live(ui_manager.get_current_layout(), refresh_per_second=10,auto_refresh=True,screen=True)
        ui_state.ui_manager = ui_manager
        
        logger.debug("Initializing input handler and keyboard listener")
        input_handler =InputHandler(ui_state=ui_state, ui_manager=ui_manager)
        keyboard_listener  = Listener(on_press= input_handler.handle_key)
        #listens for keyboard key press

        logger.info("Starting main application loop")
        with keyboard_listener:
            #Renders an auto-updating terminal
            with ui_manager.live:
                while ui_state.running: #if program has not been terminated
                    time.sleep(0.4)
            logger.debug("Stopping keyboard listener and live display")
            keyboard_listener.stop()
            ui_manager.live.stop()   
            keyboard_listener.join()
        
        # Wait for NLTK initialization thread to complete (if still running)
        if init_thread.is_alive():
            logger.info("Waiting for NLTK initialization to complete")
            init_thread.join(timeout=5.0)
            if init_thread.is_alive():
                logger.warning("NLTK initialization did not complete within timeout")
        
        logger.info("RichWord application stopped gracefully")
    
    except Exception as e:
        logger.error(f"Fatal error in main application: {e}", exc_info=True)
        raise

if __name__ == "__main__":
 
    main()