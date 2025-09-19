from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING    
from rich.layout import Layout
from abc import ABC, abstractmethod
class AppState(Enum):
    DICTIONARY = "dictionary"
    SETTINGS = "settings"
    HELP = "help"
    MENU = "menu"
    GAMES = "games"
    QUIZGAME = "quiz_game"
    GUESS_WORD_GAME = "guess_the_word_game"
    GAMES_SELECTION = "game_selection"
class DictionaryState(Enum):
    FIND = "find"
    SYNONYM = "synonym"
    RHYMING_WORDS = "rhyming_words"
    DEFINITION = "search_by_definition"
    USE_CASE = "use_case"
@dataclass
class GameState:
    score: int = 0
    total_questions: int = 0
    current_question: int = 0
@dataclass
class UIState:
    current_screen: AppState = AppState.DICTIONARY
    selected_index: int = 0
    search_query: str = ""
    show_full_definition: bool = False
    similar_words: List[str] = field(default_factory=list)
    last_found_word: Optional[str] = None
    last_found_definition: Optional[str] = None
    

class Renderer(ABC):
    """Abstract base class for different screen renderers"""
    
    @abstractmethod
    def render(self, state: UIState) -> Layout:
        """Render the UI for this screen"""
        pass