
from .abtract_render import Renderer
from rich.padding import Padding
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..ui_state import UiState
class HelpRenderer(Renderer):
    """Renders the help screen"""

    def update(self, ui_state: "UiState") -> Layout:
        layout = Layout(name="root")
        layout.split(Layout(name="main"))
        
        help_text = """
[bold]Dictionary App - Help[/bold]

[cyan]Commands:[/cyan]
• [bold]find <word>[/bold]     - Search for a word definition
• [bold]synonyms <word>[/bold] - Find synonyms for a word
• [bold]help[/bold]           - Show this help screen

[cyan]Navigation:[/cyan]
• [bold]↑/↓[/bold]            - Navigate through options
• [bold]Enter[/bold]          - Select/Execute
• [bold]Esc[/bold]            - Go to settings
• [bold]n[/bold]              - Show full definition (after search)
• [bold]Ctrl+C[/bold]         - Exit application

[cyan]Tips:[/cyan]
• Type partial words to see suggestions
• Use arrow keys to navigate similar words
• Press 'n' after a search to see the full definition
        """
        
        layout["main"].update(

           Align.center(Panel(help_text, title="[bold]Help[/bold]", border_style="green",expand=False)),

        )
        
        return layout