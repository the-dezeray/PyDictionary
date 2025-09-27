
from typing import Callable, Dict, TYPE_CHECKING
from .app_state import AppState
from rich.table import Table
from .nav import navigate
#from .ot import activate_voice
if TYPE_CHECKING:
    from .core import Core
    from .ui_manager import UIManager
class InputHandler:
    """Handles keyboard input and translates it to UI actions."""


    def __init__(self, ui_state:"Core", ui_manager:"UIManager"):
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
            #"Key.down": lambda: activate_voice(self.core),
        }
    def handle_key(self, key: str) -> None:
        """Process a keyboard event"""
        key_str = str(key).replace("'", "")

        if key_str == "Key.space": key_str = " "

        if key_str in self.key_mappings:
            self.key_mappings[key_str]()
        elif len(key_str) == 1:  # Regular character
            self._handle_character(key_str)
        #elif key_str == "n" and self.ui_manager.state.last_found_definition:
         #   self.ui_manager.toggle_full_definition()

        self.ui_manager.refresh()
    def _handle_character(self, char: str) -> None:
        """Handle regular character input"""
        if self.ui_state.table_of_results:
            self.ui_state.table_of_results = None # Clear previous results if any
        self.ui_state.current_entry_text += char
        self.ui_state.key_count += 1

        
    def _handle_enter(self) -> None:
        """Handle enter key based on current screen"""

        if self.ui_state.current_screen == AppState.MENU:
            self.ui_state.command()
        else:
            self.run_command()
            self.ui_state.current_entry_text = ""
            self.ui_state.formated_entry_text = ""
    def run_command(self):
        """runs user command """
        
        # Check if user typed 'n' to show full definition
        if self.ui_state.current_entry_text.strip().lower() == 'n':
            #self.core.show_full_definition_method()
            ...
        else:
            self.ui_state.show_full_definition = False  # Reset full definition flag
            self.ui_state.command()
    def _handle_backspace(self) -> None:
        """Handle backspace key"""
        current_query = self.ui_state.current_entry_text
        if current_query:
            self.ui_state.current_entry_text =  self.ui_state.current_entry_text[:-1]
