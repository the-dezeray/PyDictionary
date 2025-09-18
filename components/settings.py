from rich.table import Table
from rich.style import Style    
from typing import TYPE_CHECKING
from app_state import AppState,DictionaryState  
if TYPE_CHECKING:
    from core import Core


def switch_to_dictionary_screen(core: "Core"):
    """Custom function to switch to dictionary screen with additional setup"""
    core.current_screen = AppState.DICTIONARY
    # Add any additional functionality here
    # For example:
    # - Reset search query
    # - Clear previous results
    # - Log the transition
    # - Play sound effect
    # - Set default focus
    print("Switching to dictionary screen...")  # Example additional functionality


def gameSelectionTable(core:"Core"):
    def switch_to_quiz():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.QUIZGAME
        #core.command = core.PRIMARY_KEY_WORD_MAPPING["find"]
        #core.dictionary_state = DictionaryState.FIND
    options = {
        "guess the word": lambda: print("Starting 'Guess the Word'..."),  # Placeholder
        "guess the definition": lambda: print("Starting 'Guess the Definition'..."),  # Placeholder 
        "hangman": lambda: print("Starting 'Hangman'..."),  # Placeholder
        "quiz": switch_to_quiz,
        "back": lambda: setattr(core, 'current_screen', AppState.MENU)
    }
    table = Table.grid(expand=True)
    core.selected = core.selected % len(options)
    
    # Get the keys as a list to access by index
    option_keys = list(options.keys())
    
    for index, key in enumerate(option_keys):
        if index == core.selected:
            # Fix the closure issue by capturing the current function value
            selected_function = options[key]
            core.command = selected_function
            table.add_row(f"[bold blue]{key}[/bold blue]", style=Style(color="blue"))
        else:
            table.add_row(key)
    return table
def getTable(core:"Core"):
    """returns the current table object"""
    # Define all options as callable functions

    def switch_to_dictionary():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.DICTIONARY
        core.command = core.PRIMARY_KEY_WORD_MAPPING["find"]
        core.dictionary_state = DictionaryState.FIND
    def switch_to_synonyms():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.DICTIONARY
        core.command = core.PRIMARY_KEY_WORD_MAPPING["synonym"]
        core.dictionary_state = DictionaryState.SYNONYM
    def switch_to_rhymes():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.DICTIONARY
        core.command = core.PRIMARY_KEY_WORD_MAPPING["rhyming_words"]
        core.dictionary_state = DictionaryState.RHYMING_WORDS
    def switch_to_use_case():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.DICTIONARY
        core.command = core.PRIMARY_KEY_WORD_MAPPING["use_case"]
        core.dictionary_state = DictionaryState.USE_CASE
    def switch_to_definitions():
        """Switch to dictionary screen with optional additional setup"""
        core.current_screen = AppState.DICTIONARY
        core.command = core.PRIMARY_KEY_WORD_MAPPING["search_by_definition"]
        core.dictionary_state = DictionaryState.DEFINITION
    switch_to_synonyms = lambda: print("Switching to synonyms...")  # Placeholder
    switch_to_games =  lambda: setattr(core, 'current_screen', AppState.GAMES_SELECTION)
    
    switch_to_help= lambda : setattr(core, 'current_screen', AppState.HELP)
    options = {
        "find": switch_to_dictionary,
        "search by definition": switch_to_definitions,
        "synonyms": switch_to_synonyms,
        "rhymes": switch_to_rhymes,
        "games": switch_to_games,
        "use-case": switch_to_use_case,
        "help": switch_to_help
    }
    
    table = Table.grid(expand=True)
    core.selected = core.selected % len(options)
    
    # Get the keys as a list to access by index
    option_keys = list(options.keys())
    
    for index, key in enumerate(option_keys):
        if index == core.selected:
            # Fix the closure issue by capturing the current function value
            selected_function = options[key]
            core.command = selected_function
            table.add_row(f"[bold blue]{key}[/bold blue]", style=Style(color="blue"))
        else:
            table.add_row(key)
    return table