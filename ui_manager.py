
from app_state import AppState, UIState
from typing import Dict,TYPE_CHECKING
from renderers.dictionary import DictionaryRenderer
from renderers.menu import MenuRenderer
from renderers.help import HelpRenderer
from renderers.abtract_render import Renderer
from renderers.settings import SettingsRenderer
from renderers.game_selection import GameSelectionRenderer
from renderers.quiz_game import QuizGameRenderer
from rich.layout import Layout
if TYPE_CHECKING:
    from rich.live import Live
class UIManager:
    """Manages UI state and rendering coordination"""
    
    def __init__(self,core):
        self.core = core
        self.live : "Live|None" 
        self.ui_state = UIState()

        # Create renderers for each screen
        self.renderers: Dict[AppState, Renderer] = {
            AppState.DICTIONARY: DictionaryRenderer(core=core),
            AppState.SETTINGS: ... , #SettingsRenderer(core=core),
            AppState.HELP: HelpRenderer(core=core),
            AppState.MENU:  MenuRenderer(core=core),
            AppState.GAMES: ... , #GamesRenderer(core=core),
            AppState.GAMES_SELECTION: GameSelectionRenderer(core=core),
            AppState.QUIZGAME: QuizGameRenderer(core=core),

        }
    def switch_screen(self, new_screen: AppState):
        """Switch to a different screen"""
        if new_screen in self.renderers:
            self.core.current_screen = new_screen
            self.refresh()
    def get_current_layout(self) -> Layout:
        """Get the layout for the current screen"""
        renderer = self.renderers[self.core.current_screen]
        return renderer.update(self.core)
    def refresh(self):
        """Refresh the UI"""

        self.live.update(self.get_current_layout()) 