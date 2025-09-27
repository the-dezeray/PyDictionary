"""Command handlers for different dictionary operations - Refactored for code reuse"""

from rich.panel import Panel
from .text_utils import extract_last_word
from .core import Core
from rich.panel import Panel
from .util.text_to_speach import text_to_speech
from .components.display_builders import (
    build_definition_panel, 
    build_not_found_message, 
    create_results_table,
    create_loading_table
)
from .dictionary import dictionary_service
from .util.format_text import format_definition
from typing import Any, Optional, List, Callable, Tuple


def find_word_definition(word_to_find: str):
    """Find word definition in dictionary"""
    return dictionary_service.find_word_definition(word_to_find)


# Base helper functions for common patterns
def _create_results_panel(content: str, title: str, content_color: str = "green") -> Panel:
    """Create a standardized results panel"""
    return Panel(
        f"[{content_color}]{content}[/{content_color}]",
        title=f"[bold yellow]{title}[/bold yellow]",
        title_align="left",
        expand=True
    )


def _create_not_found_message(search_term: str, item_type: str, additional_info: str = "") -> str:
    """Create a standardized 'not found' message"""
    base_message = f"[grey]No {item_type} found for [green]{search_term}[/green]"
    if additional_info:
        base_message += f"\n[i]{additional_info}[/i]"
    base_message += "[/grey]"
    return base_message


def _execute_search_command(
    ui_state: Any,
    search_function: Callable[[str], Any],
    result_formatter: Callable[[str, Any], Tuple[Optional[Panel], Optional[str]]],
    loading_message: str = "",
    use_full_text: bool = False
):
    """
    Generic function to execute search commands with common pattern:
    1. Show loading (if specified)
    2. Extract search term
    3. Execute search
    4. Format and display results
    """
    # Show loading if specified
    if loading_message:
        ui_state.table_of_results = create_loading_table(loading_message)
        ui_state.ui_manager.refresh()
    
    # Extract search term
    if use_full_text:
        search_term = ui_state.current_entry_text.strip()
    else:
        search_term = extract_last_word(ui_state.current_entry_text)
    
    # Handle empty input
    if not search_term:
        table = create_results_table()
        table.add_row("[grey]Please enter a search term[/grey]")
        ui_state.table_of_results = table
        return
    
    # Create results table
    table = create_results_table()
    
    # Execute search
    results = search_function(search_term)
    
    # Format results
    panel, error_message = result_formatter(search_term, results)
    
    if panel:
        table.add_row(panel)
    else:
        table.add_row(error_message)
    
    ui_state.table_of_results = table


# Result formatters for different command types
def _format_definition_results(search_term: str, results: Tuple[str, str]) -> Tuple[Optional[Panel], Optional[str]]:
    """Format definition search results"""
    word, definition = results
    if word and definition:
        # This needs access to ui_state, so we'll handle this case separately
        return None, None  # Special handling needed
    else:
        error_msg = build_not_found_message(search_term)
        return None, error_msg


def _format_list_results(search_term: str, results: List[str], result_type: str, additional_info: str = "") -> Tuple[Optional[Panel], Optional[str]]:
    """Format results that are lists of words (synonyms, rhymes, etc.)"""
    if results:
        content = ", ".join(results)
        title = f"{result_type} for '{search_term}'"
        panel = _create_results_panel(content, title)
        return panel, None
    else:
        error_msg = _create_not_found_message(search_term, result_type.lower(), additional_info)
        return None, error_msg


# Refactored command functions
def find(ui_state: Any):
    """Find word in dictionary and update renderable to display result"""
    last_word = extract_last_word(ui_state.current_entry_text)
    table = create_results_table()
    
    # Find the word definition
    word, definition = find_word_definition(last_word)
    
    if word and definition:
        ui_state.current_word = word
        ui_state.current_definition = definition
        # Format the definition
        formatted_definition = format_definition(definition)
        
        # Build the panel
        panel = build_definition_panel(word, formatted_definition, ui_state)
        table.add_row(panel)
    else:
        # Build not found message
        not_found_message = build_not_found_message(last_word)
        table.add_row(not_found_message)

    ui_state.table_of_results = table


def synonyms(ui_state: Any):
    """Find synonyms for a word and update renderable to display results"""
    from .kn import get_synonyms
    
    def format_synonyms(search_term: str, results: List[str]) -> Tuple[Optional[Panel], Optional[str]]:
        return _format_list_results(
            search_term, 
            results, 
            "Synonyms", 
            "Word maybe existing but not present in the database"
        )
    
    _execute_search_command(
        ui_state,
        get_synonyms,
        format_synonyms,
        "Finding Synonyms..."
    )


def search_by_definition(ui_state: Any):
    """Find words that match a given meaning/definition using Datamuse API"""
    from .kn import search_words_by_meaning
    
    def format_meaning_results(search_term: str, results: List[str]) -> Tuple[Optional[Panel], Optional[str]]:
        if results:
            content = ", ".join(results)
            title = f"Words matching '{search_term}'"
            panel = _create_results_panel(content, title)
            return panel, None
        else:
            error_msg = f"[grey]No words found matching '[green]{search_term}[/green]'\n[i]Try rephrasing your search or use simpler terms[/i][/grey]"
            return None, error_msg
    
    _execute_search_command(
        ui_state,
        search_words_by_meaning,
        format_meaning_results,
        "Searching for words...",
        use_full_text=True
    )


def rhyming_words(ui_state: Any):
    """Find rhyming words and update renderable to display results"""
    from .kn import get_rhyming_words
    
    def format_rhymes(search_term: str, results: List[str]) -> Tuple[Optional[Panel], Optional[str]]:
        return _format_list_results(search_term, results, "Rhyming words")
    
    _execute_search_command(
        ui_state,
        get_rhyming_words,
        format_rhymes
    )


def dictionary(core: Any):
    """Dictionary command placeholder"""
    ...


def use_case(core: Any):
    """Use case command placeholder (games)"""
    ...


def help_command(core: Any):
    """Help command placeholder"""
    ...

def activate_voice(ui_state:"Core"):
    ui_state.instruction = Panel("Voice Activated\n [cyan]|||||[/cyan]")
    word = ui_state.current_word
    definition = ui_state.current_definition
    ui_state.voice_activate = True
    if word and definition:

        text_to_speech(f"{word}")

