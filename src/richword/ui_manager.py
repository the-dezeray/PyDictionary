
from .app_state import AppState
from typing import Dict,TYPE_CHECKING
from .util.logger import get_logger
from .renderers.dictionary import DictionaryRenderer
from .renderers.menu import MenuRenderer
from .renderers.help import HelpRenderer
from .renderers.abtract_render import Renderer
from .renderers.settings import SettingsRenderer
from .renderers.game_selection import GameSelectionRenderer
from .renderers.quiz_game import QuizGameRenderer
from rich.layout import Layout
from .renderers.guess_word import GuessWordGameRenderer
if TYPE_CHECKING:
    from .ui_state import UiState
    from rich.live import Live

logger = get_logger(__name__)
class UIManager:
    """Manages UI state and rendering coordination"""
    
    def __init__(self,ui_state:"UiState"):
        logger.debug("Initializing UIManager")
        ui_state.ui_manager = self
        self.live : "Live" 
        self.ui_state = ui_state

        logger.debug("Creating renderers for each application screen")
        # Create renderers for each screen
        self.renderers: Dict[AppState, Renderer] = {
            AppState.DICTIONARY: DictionaryRenderer(ui_state),
            AppState.SETTINGS: SettingsRenderer(ui_state),
            AppState.HELP: HelpRenderer(ui_state),
            AppState.MENU:  MenuRenderer(ui_state),
            AppState.GAMES:  QuizGameRenderer(ui_state),
            AppState.GAMES_SELECTION: GameSelectionRenderer(ui_state),
            AppState.QUIZGAME: QuizGameRenderer(ui_state),
            AppState.GUESS_WORD_GAME: GuessWordGameRenderer(ui_state),
        }
    def switch_screen(self, new_screen: AppState):
        """Switch to a different screen"""
        if new_screen in self.renderers:
            self.ui_state.current_screen = new_screen
            self.refresh()
    def get_current_layout(self) -> Layout:
        """Get the layout for the current screen"""
        renderer = self.renderers[self.ui_state.current_screen]
        return renderer.update(self.ui_state)
    def refresh(self):
        """Refresh the UI"""

        self.live.update(self.get_current_layout()) 