"""the core module"""
import json
from rapidfuzz import fuzz, process
import re
from rich.table import Table
from rich.layout import Layout
from rich.layout import Layout
from rich.padding import Padding
from rich.style import Style
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from app_state import AppState,DictionaryState
from dictionary import dictionary_service
def count_words_in_definition(text):
        """Count words in definition text, ignoring Rich markup tags"""
        # Remove Rich markup tags like [bold], [/bold], [italic], etc.
        clean_text = re.sub(r'\[/?[a-zA-Z0-9\s]*\]', '', str(text))
        # Split by whitespace and count non-empty parts
        words = clean_text.split()
        return len([word for word in words if word.strip()])
class Core():
    """process keyboard inputs/commands and updating layout appearance""" 

    def __init__(self) -> None:
        self.PRIMARY_KEY_WORD_MAPPING = {
            "find":lambda: find(self),
            "search_by_definition":lambda: search_by_definition(self),
            "synonym":lambda: synonyms(self),
            "rhyming_words":lambda: rhyming_words(self),
            "use_case":lambda: use_case(self),
            "games":lambda: use_case(self),
            "help":lambda: help(self),
            "exit":lambda: exit(0)
            }

        #Core Related
        self.current_entry_text :str= ""
        self.clayout  =None
        self.formated_entry_text :str = ""
        self.suggestion :str = "" 
        self.running :str = True
        self.split_entry_text= ""
        self.selected :int = 0
        self.max_displayed_similar_words :int = 6
        self.word_limit :int = 50  # Maximum words before truncating definition
        self.show_full_definition :bool = False  # Flag for showing full definition
        self.last_found_definition :str = ""  # Store full definition for 'n' command
        self.last_found_word :str = ""  # Store the word for full definition display
        #Layout related 
        self.table :Table = Table()
        self.live : Live
        self.table_of_results :Table = None
        self.dictionary_state :DictionaryState = DictionaryState.FIND# Current state in dictionary (e.g., 'find', 'synonym')   
        self.command : callable = lambda: find(self)
        self.current_screen : AppState= AppState.DICTIONARY
        self.key_count :int = 0

    def navigate(self,direction:str):
        """navigate through menu options"""
        if direction == "up":
            self.selected -= 1
        elif direction == "down":
            self.selected += 1




def dictionary(core):
    ...
def use_case(core):
    ...
def help(core):
    ...
def synonyms(core):
    ...

def use_case(core):
    ...
def search_by_definition(core):
    ...
    
def rhyming_words(core):
    ...

from util.format_text import truncate_definition , format_definition


def find_word_definition(word_to_find):
    """Find word definition in dictionary"""
    return dictionary_service.find_word_definition(word_to_find)


def build_definition_panel(word, formatted_definition, core):
    """Build Rich panel for displaying definition"""
    # Store full definition for potential 'n' command
    core.last_found_definition = str(formatted_definition)
    core.last_found_word = word
    
    # Check if definition needs truncation
    word_count = count_words_in_definition(formatted_definition)
    if word_count > core.word_limit and not core.show_full_definition:
        truncated_text, was_truncated = truncate_definition(formatted_definition, core.word_limit)
        if was_truncated:
            display_text = f"{truncated_text}\n\n[dim yellow]Definition truncated ({word_count} words). Type 'n' for full definition.[/dim yellow]"
        else:
            display_text = formatted_definition
    else:
        display_text = formatted_definition

    return Panel(
        display_text,
        title=f"[bold yellow]{word}[/bold yellow]",
        title_align="left",
        expand=True
    )

def build_not_found_message(word):
    """Build message for word not found"""
    return f"[grey] [green]{word}[/green] not found  \n [i] Word maybe existing but not present in the database[/i][/grey]"

def find(core):
    """Find word in dictionary and update renderable to display result"""
    split_entry_text = core.current_entry_text.split(" ")
    last_word = split_entry_text[-1]
    
    if last_word == "" and len(split_entry_text) > 1:
        last_word = split_entry_text[-2]
    
    table = Table(expand=True, show_edge=False)
    table.add_column()
    
    # Find the word definition
    word, definition = find_word_definition(last_word)
    
    if word and definition:
        # Format the definition
        formatted_definition = format_definition(definition)
        
        # Build the panel
        panel = build_definition_panel(word, formatted_definition, core)
        table.add_row(panel)
    else:
        # Build not found message
        not_found_message = build_not_found_message(last_word)
        table.add_row(not_found_message)
    
    core.table_of_results = table