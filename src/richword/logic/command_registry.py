"""Command registry for mapping command names to functions"""

from typing import Dict, Callable, Any
from . import commands


def get_command_mapping(core_instance: Any) -> Dict[str, Callable[[], None]]:
    """Get the mapping of command names to their corresponding functions"""
    return {
        "find": lambda: commands.find(core_instance),
        "search_by_definition": lambda: commands.search_by_definition(core_instance),
        "synonym": lambda: commands.synonyms(core_instance),
        "rhyming_words": lambda: commands.rhyming_words(core_instance),
        "games": lambda: commands.use_case(core_instance),
        "help": lambda: commands.help_command(core_instance),
        "exit": lambda: exit(0)
    }