from rich.table import Table
from rich.panel import Panel
def show_full_definition_method(self):
    """Handle the 'n' command to show full definition"""
    if self.last_found_definition and self.last_found_word:
        self.table = Table(expand=True, show_edge=False)
        self.table.add_column()
        
        panel = Panel(
            self.last_found_definition,
            title=f"[bold yellow]{self.last_found_word}[/bold yellow] [dim](Full Definition)[/dim]",
            title_align="left",
            expand=True
        )
        self.table.add_row(panel)
    else:
        self.table = Table(expand=True, show_edge=False)
        self.table.add_column()
        self.table.add_row("[dim red]No recent definition to expand.[/dim red]")
    