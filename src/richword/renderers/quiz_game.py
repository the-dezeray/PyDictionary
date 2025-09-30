import random
from typing import TYPE_CHECKING

from .base_game_renderer import BaseGameRenderer
from .dictionary_services import DictionaryService

if TYPE_CHECKING:
    from ..ui_state import UiState


class QuizGameRenderer(BaseGameRenderer):
    def __init__(self, ui_state: "UiState") -> None:
        super().__init__(ui_state)
        self.name = "QuizGame"
        self.random_word = ""

    def refresh(self):
        """Refresh game data with a new word and random meaning options"""
        self.random_word, meaning = DictionaryService.get_word_of_the_day()
        random_index = random.randint(0, 3)
        # Get random meanings as tuples and extract just the meanings (second element)
        random_meaning_tuples = DictionaryService.get_random_meanings(3)
        random_meanings = [meaning_tuple[1] for meaning_tuple in random_meaning_tuples]
        
        self.options = [{meaning: self.wrong_answer} for meaning in random_meanings]
        self.options.insert(random_index, {meaning: self.correct_answer})
        # Reset the answer status when refreshing
        self.iscorrect = None

    def get_main_content(self) -> str:
        """Get the word to display as the main content"""
        return self.random_word
