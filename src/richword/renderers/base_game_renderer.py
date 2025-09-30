"""Base Game Renderer Module

This module provides a base class for game renderers that eliminates redundancy
between different game types like QuizGame and GuessWordGame.
"""

from abc import abstractmethod
from typing import Callable, List, Dict, Optional, TYPE_CHECKING
import threading
import time
from rich.panel import Panel
from .abtract_render import Renderer
from ..components.layouts import menu_layout
from ..components.settings import quizTable
from rich.style import Style
if TYPE_CHECKING:
    from ..ui_state import UiState
    from rich.layout import Layout


class BaseGameRenderer(Renderer):
    """Base class for game renderers with common functionality"""
    
    def __init__(self, ui_state: "UiState") -> None:
        super().__init__(ui_state)
        self.ui_state = ui_state
        self.name = "GameLayout"
        self.iscorrect: Optional[bool] = None
        self.options: List[Dict[str, Callable]] = []
        self.timer_thread: Optional[threading.Thread] = None
        self.timer_running = False
        self.refresh_interval = 3  # 3 seconds
        self.words_per_game = 10
        self.attempted_words = 0
        self.refresh()

    def start_timer(self):
        """Start the timer thread for auto-refresh"""
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()

    def stop_timer(self):
        """Stop the timer thread"""
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        
    def _timer_loop(self):
        """Timer loop that runs in a separate thread"""
        while self.timer_running:
            time.sleep(self.refresh_interval)
            if self.timer_running:
                self.refresh()
                # Call UI manager refresh to update the display
                if self.ui_state.ui_manager:
                    self.ui_state.ui_manager.refresh()
                self.timer_running = False

    def wrong_answer(self):
        """Handle wrong answer - decrease score and start timer"""
        self.ui_state.game_state.score -= 1
        self.iscorrect = False
        self.start_timer()
        # Immediately update the UI to show the wrong answer feedback
        if self.ui_state.ui_manager:
            self.ui_state.ui_manager.refresh()
            
    def correct_answer(self):
        """Handle correct answer - increase score and start timer"""
        self.ui_state.game_state.score += 1
        self.iscorrect = True
        self.start_timer()
        # Immediately update the UI to show the correct answer feedback
        if self.ui_state.ui_manager:
            self.ui_state.ui_manager.refresh()

    @abstractmethod
    def refresh(self):
        """Refresh game data - must be implemented by subclasses"""
        pass

    @abstractmethod
    def get_main_content(self) -> str:
        """Get the main content to display - must be implemented by subclasses"""
        pass

    def update(self, ui_state: "UiState") -> "Layout":
        """Update the layout with game content"""
        layout = menu_layout()
        from rich.console import Group
        from rich.align import Align
        from rich.padding import Padding

        main_content = Align(
            renderable=Padding(self.get_main_content(), pad=(0, 20)),
            align="center"
        )
        
        # Status message based on answer correctness
        if self.iscorrect is None:
            status_flag = "[yellow]CHOOSE[/yellow]"
        elif self.iscorrect:
            status_flag = Panel(renderable="[green]          Correct!              [/green]", style=Style(bgcolor="green"),expand=True,subtitle="+1")
        else:
            status_flag = Panel(renderable="[red]      wrong!      [/red]", border_style="red",expand =True,subtitle="-1")

        renderable = Group(
            Align(f"Score: {self.ui_state.game_state.score} ", align="right", ),
            Align.center(Padding(main_content, expand=False, style=Style(bgcolor="cyan"))),
            Padding("\n\n"),
            Align.center(quizTable(self.ui_state, options=self.options)),
            Padding("\n\n"),
            Align.center(status_flag ),

        )
        layout["main"].update(renderable=Align.center(renderable, vertical="middle"))
        return layout

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.stop_timer()