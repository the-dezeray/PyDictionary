
from typing import Callable, Dict, TYPE_CHECKING
from app_state import AppState
from ot import activate_voice
if TYPE_CHECKING:
    from core import Core
    from ui_manager import UIManager
class InputHandler:
    """Handles keyboard input and translates it to UI actions."""


    def __init__(self, core:"Core", ui_manager:"UIManager"):
        self.core = core
        self.ui_manager = ui_manager

        # Map special keys to actions
        self.key_mappings: Dict[str, Callable[[], None]] = {
            #'Key.up': self.ui_manager.navigate_up,
            #'Key.down': self.ui_manager.navigate_down,
            #'Key.esc': lambda: self.ui_manager.switch_screen(AppState.SETTINGS),
            'Key.enter': self._handle_enter,
            'Key.backspace': self._handle_backspace,
            'Key.tab': lambda: self.ui_manager.switch_screen(AppState.MENU),  # Ignore tab key
            "Key.up": lambda: core.navigate("up"),
            "Key.down": lambda: core.navigate("down"),
            "Key.right": lambda: activate_voice(core),
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
        if self.core.table_of_results:
            self.core.table_of_results = None  # Clear previous results if any
        self.core.current_entry_text += char
        self.core.key_count += 1

        
    def _handle_enter(self) -> None:
        """Handle enter key based on current screen"""
        from app_state import AppState
        if self.core.current_screen == AppState.MENU:
            self.core.command()
        else:
            self.run_command()
            self.core.current_entry_text = ""
            self.core.formated_entry_text = ""
    def run_command(self):
        """runs user command """
        
        # Check if user typed 'n' to show full definition
        if self.core.current_entry_text.strip().lower() == 'n':
            #self.core.show_full_definition_method()
            ...
        else:
            self.core.show_full_definition = False  # Reset full definition flag
            self.core.command()
    def _handle_backspace(self) -> None:
        """Handle backspace key"""
        current_query = self.core.current_entry_text
        if current_query:
            self.core.current_entry_text =  self.core.current_entry_text[:-1]
    # def handle_key(self, key_event: str) -> None:

    #     input_string :str= str(key_event)
    #     input_string = input_string.replace("'","")
        
    #     match input_string:
    #         case "Key.down":    
    #             self.core.selected += 1
    #         case "Key.up":
    #             self.core.selected -= 1
    #         case "Key.space":
    #             input_string = " "
            
    #         case "Key.backspace":
    #             input_string = ""
    #             self.core.current_entry_text =  self.core.current_entry_text[:-1]
    #             self.core.key_count = max(0,self.core.key_count - 1)
    #         #RUN COMMAND
    #         case "Key.enter":
    #             if self.core.clayout.name == "SettingTab":
    #                 self.core.selected_function()
                    
    #             else:
    #                 self.core.run_command()
    #                 self.core.current_entry_text = ""
    #                 self.core.formated_entry_text = ""
    #         case "Key.esc":
    #            from customLayouts import SettingTab
    #            self.core.clayout = SettingTab(self.core)

    #         #default
    #         case _:
    #             pass

    #     if len(input_string) <2: #<- prevents execution of unmapped keys !dont touch
    #         self.core.current_entry_text += input_string
    #         self.core.key_count += 1

    #     self.core.live.update(self.core.clayout.update(self.core))