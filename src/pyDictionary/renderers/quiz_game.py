from .abtract_render import Renderer
from ..components.layouts import settings_layout,menu_layout
from rich.layout import Layout
from rich.panel import Panel
import random
import threading
import time
from ..components.settings import getTable,quizTable
from .dictionary_services import DictionaryService 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core import Core
class QuizGameRenderer(Renderer):
    def __init__(self,core:"Core") -> None:
        super().__init__(core)
        self.core = core
        self.name = "MenuLayout"
        self.iscorrect = None
        self.random_word = ""
        self.options : list[dict[str, callable]] = []
        self.timer_thread = None
        self.timer_running = False
        self.refresh_interval = 3  # 30 seconds
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
                if self.core.ui_manager:
                    self.core.ui_manager.refresh()
                    self.stop_timer()
    def wrong_answer(self):
        self.core.game_state.score -= 1
        self.iscorrect = False
        self.start_timer()
        # Immediately update the UI to show the wrong answer feedback
        if self.core.ui_manager:
            self.core.ui_manager.refresh()
            
    def correct_answer(self):
        self.core.game_state.score += 1
        self.answer_status = "correct"
        self.iscorrect = True
        self.start_timer()
        # Immediately update the UI to show the correct answer feedback
        if self.core.ui_manager:
            self.core.ui_manager.refresh()
    def refresh(self):
        self.random_word, meaning = DictionaryService.get_word_of_the_day()
        random_index = random.randint(0, 3)
        random_meanings = DictionaryService.get_random_meanings(3) 
        self.options = [{word:self.wrong_answer} for word  in random_meanings]
        self.options.insert(random_index,{meaning:self.correct_answer})
        # Reset the answer status when refreshing
        self.iscorrect = None

    def update(self,core)->Layout:
        layout = menu_layout()
        from rich.console import Group
        from rich.align import Align
        from rich.padding import Padding
        from art import text2art

        word = Align(renderable= Padding(self.random_word),align="center", pad=(0, 20))
        if self.iscorrect is None:
            flag = "[yellow]Select an answer[/yellow]"
        elif self.iscorrect:
            flag = "[green]Correct![/green]"
        else:
            flag = "[red]Wrong![/red]"
        renderable = Group(word,quizTable(self.core,options=self.options),  Align(flag,align="center"))
        layout["main"].update(renderable=renderable)
        return layout

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.stop_timer()
