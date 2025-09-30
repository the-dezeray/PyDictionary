import random
from typing import TYPE_CHECKING

from .base_game_renderer import BaseGameRenderer
from .dictionary_services import DictionaryService

if TYPE_CHECKING:
    from ..ui_state import UiState


class GuessWordGameRenderer(BaseGameRenderer):
    def __init__(self, ui_state: "UiState") -> None:
        super().__init__(ui_state)
        self.name = "GuessWordGame"
        self.random_word = ""
        self.score = 0
        self.word_count =0
        self.words_per_game = 12


    def refresh(self):
        """Refresh game data with a new word and meaning"""
        self.random_word, self.meaning = DictionaryService.get_word_of_the_day()
        random_index = random.randint(0, 3)
        # Get multiple random words for options
        random_words = [DictionaryService.get_word_of_the_day()[0] for _ in range(3)]
        self.options = [{word: self.wrong_answer} for word in random_words]
        self.options.insert(random_index, {self.random_word: self.correct_answer})
        # Reset the answer status when refreshing
        self.iscorrect = None

    def get_main_content(self) -> str:
        """Get the meaning to display as the main content"""
        return self.meaning
