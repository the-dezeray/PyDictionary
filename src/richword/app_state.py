from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING    


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

    

