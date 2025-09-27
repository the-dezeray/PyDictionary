"""the core module"""

from rich.table import Table
from rich.padding import Padding
from rich.align import Align

from .app_state import AppState, DictionaryState, GameState
from .command_registry import get_command_mapping
from . import commands
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from rich.console import RenderableType
    from .ui_manager import UIManager
class Core():
    """process keyboard inputs/commands and updating layout appearance""" 

    def __init__(self) -> None:
        self.PRIMARY_KEY_WORD_MAPPING = get_command_mapping(self)

        #Core Related
        self.current_entry_text :str= ""
        self.clayout  =65
        self.formated_entry_text :str = ""
        self.suggestion :str = "" 
        self.running :bool = True
        self.split_entry_text= ""
        self.selected :int = 0
        self.max_displayed_similar_words :int = 6
        self.word_limit :int = 50  # Maximum words before truncating definition
        self.show_full_definition :bool = False  # Flag for showing full definition
        self.last_found_definition :str = ""  # Store full definition for 'n' command
        self.last_found_word :str = ""  # Store the word for full definition display
        #Layout related 
        self.table :Table = Table()
        self.voice_activate= False
        self.ui_manager :UIManager
        self.table_of_results :Table|None = None
        self.dictionary_state :DictionaryState = DictionaryState.FIND# Current state in dictionary (e.g., 'find', 'synonym')
        self.command : Callable[[],None] = lambda: commands.find(self)
        self.current_screen : AppState= AppState.DICTIONARY
        self.key_count :int = 0
        self.game_state = GameState() 
        self.current_word = ""
        self.current_definition = ""
        self.instruction : RenderableType= Align.center(Padding("[cyan]space[/cyan]: to activate voice"),vertical="bottom")


