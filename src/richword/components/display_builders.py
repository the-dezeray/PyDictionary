"""Display builders for creating Rich UI components"""

from rich.table import Table
from rich.panel import Panel
from ..util.format_text import truncate_definition
from ..text_utils import count_words_in_definition
from typing import Any


def build_definition_panel(word: str, formatted_definition: Any, ui_state: Any) -> Panel:
    """Build Rich panel for displaying definition"""
    # Store full definition for potential 'n' command
    ui_state.last_found_definition = str(formatted_definition)
    ui_state.last_found_word = word
    
    # Check if definition needs truncation
    word_count = count_words_in_definition(formatted_definition)
    if word_count > ui_state.word_limit and not ui_state.show_full_definition:
        truncated_text, was_truncated = truncate_definition(formatted_definition, ui_state.word_limit)
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


def build_not_found_message(word: str) -> str:
    """Build message for word not found"""
    return f"[grey] [green]{word}[/green] not found  \n [i] Word maybe existing but not present in the database[/i][/grey]"


def create_results_table() -> Table:
    """Create a standard results table"""
    table = Table(expand=True, show_edge=False)
    table.add_column()
    return table


def create_loading_table(message: str = "Loading...") -> Table:
    """Create a loading table with spinner"""
    from rich.align import Align
    from rich.spinner import Spinner
    
    loading_table = Table.grid()
    loading_table.add_column()
    loading_table.add_row(Align.center(Spinner("dots", text=message)))
    return loading_table