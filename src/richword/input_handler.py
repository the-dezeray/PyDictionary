
from typing import Callable, Dict, TYPE_CHECKING
from .app_state import AppState
from .util.logger import get_logger
from .util.nav import navigate
#from .ot import activate_voice
if TYPE_CHECKING:
    from .ui_state import UiState
    from .ui_manager import UIManager

logger = get_logger(__name__)
class InputHandler:
    """Handles keyboard input and translates it to UI actions."""


    def __init__(self, ui_state:"UiState", ui_manager:"UIManager"):
        logger.debug("Initializing InputHandler")
        self.ui_state = ui_state
        self.ui_manager = ui_manager

        # Map special keys to actions
        self.key_mappings: Dict[str, Callable[[], None]] = {
            #'Key.up': self.ui_manager.navigate_up,
            #'Key.down': self.ui_manager.navigate_down,
            #'Key.esc': lambda: self.ui_manager.switch_screen(AppState.SETTINGS),
            'Key.enter': self._handle_enter,    
            'Key.backspace': self._handle_backspace,
            'Key.tab': lambda: self.ui_manager.switch_screen(AppState.MENU),  # Ignore tab key
            "Key.up": lambda: navigate(ui_state,"up"),
            "Key.down": lambda: navigate(ui_state,"down"),
            "Key.esc": lambda: setattr(ui_state, 'running', False),  # Graceful exit
            #"Key.down": lambda: activate_voice(self.core),
        }
        logger.debug(f"InputHandler initialized with {len(self.key_mappings)} key mappings")
    def handle_key(self, key: str) -> None:
        """Process a keyboard event"""
        try:
            key_str = str(key).replace("'", "")
            logger.debug(f"Processing key: {key_str}")

            if key_str == "Key.space":
                key_str = " "

            if key_str in self.key_mappings:
                logger.debug(f"Executing mapped action for key: {key_str}")
                self.key_mappings[key_str]()
            elif len(key_str) == 1:  # Regular character
                logger.debug(f"Processing character input: {key_str}")
                self._handle_character(key_str)
            #elif key_str == "n" and self.ui_manager.state.last_found_definition:
             #   self.ui_manager.toggle_full_definition()

            self.ui_manager.refresh()
        except Exception as e:
            logger.error(f"Error handling key {key}: {e}", exc_info=True)
    def _handle_character(self, char: str) -> None:
        """Handle regular character input"""
        logger.debug(f"Adding character '{char}' to current entry")
        if self.ui_state.table_of_results:
            logger.debug("Clearing previous search results")
            self.ui_state.table_of_results = None # Clear previous results if any
        self.ui_state.current_entry_text += char
        self.ui_state.key_count += 1
        logger.debug(f"Current entry text: '{self.ui_state.current_entry_text}'")

        
    def _handle_enter(self) -> None:
        """Handle enter key based on current screen"""
        logger.debug(f"Enter key pressed on screen: {self.ui_state.current_screen}")

        if self.ui_state.current_screen == AppState.MENU:
            logger.debug("Executing menu command")
            self.ui_state.command()
        else:
            logger.debug("Running dictionary command")
            self.run_command()
            self.ui_state.current_entry_text = ""
            self.ui_state.formated_entry_text = ""
            

    def run_command(self):
        """runs user command """
        current_text = self.ui_state.current_entry_text.strip()
        logger.info(f"Running command for input: '{current_text}'")
        
        # Check if user typed 'n' to show full definition
        if current_text.lower() == 'n':
            logger.debug("User requested full definition display")
            #self.core.show_full_definition_method()
            ...
        else:
            logger.debug("Resetting full definition flag and executing command")
            self.ui_state.show_full_definition = False  # Reset full definition flag
            self.ui_state.command()
    def _handle_backspace(self) -> None:
        """Handle backspace key"""
        current_query = self.ui_state.current_entry_text
        if current_query:
            self.ui_state.current_entry_text =  self.ui_state.current_entry_text[:-1]
