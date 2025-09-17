
from app_state import AppState, UIState,CustomLayout
from typing import Dict,TYPE_CHECKING
from dictionary_renderer import DictionaryLayout
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
        self.renderers: Dict[AppState, CustomLayout] = {
            AppState.DICTIONARY: DictionaryLayout(core=core),

        }
    
    def get_current_layout(self) -> Layout:
        """Get the layout for the current screen"""
        renderer = self.renderers[AppState.DICTIONARY]
        return renderer.update(self.core)
    def refresh(self):
        """Refresh the UI"""

        self.live.update(self.get_current_layout()) 