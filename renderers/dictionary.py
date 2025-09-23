from rich.layout import Layout
from art import text2art
from rich.panel import Panel
from rich.padding import Padding
from  components.layouts import main_layout
from core import Core
from rich.table import Table
from rich.style import Style
from renderers.abtract_render import Renderer
from renderers.dictionary_services import DictionaryService


class DictionaryRenderer(Renderer):
    def __init__(self, core):
        super().__init__(core)
        self.core = core
        self.name = "DictionaryLayout"
        self.f = 0
        
        # Initialize static dictionary service
        DictionaryService.initialize()
        self.suggestion = "Enter a command"
    def format_text(self,core: Core):
        """formats the current user-input to highlight primary keys tags and text"""

        string_list =core.current_entry_text.split(" ")
        for index ,i in enumerate(string_list):
            if i in self.core.PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[code ] "  + i.upper() + "[/code]"
            if i in self.core.PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[blue] "  + i + ": [/blue]"
        formated_entry_text = " ".join(string_list)
        return formated_entry_text
    def edit_suggestion(self, core: Core):
        """Updates the suggestion renderable-object as input is updated"""
        suggestion = DictionaryService.get_suggestion(core.dictionary_state.value)
        return suggestion
    def update(self,core: Core):

        layout = main_layout()
        if core.key_count == 0:
         
            (word,meaning) = self.get_word_of_the_day()
            art = text2art(f"{word}",font="tarty4")
            from rich.align import Align
            word = Align(f"[green]{art}[/green]",align="center")
            meaning = Align(f"[dim green]\n\n{meaning}[/dim green]",align="center")
            from rich.console import Group
            a = Group(word,meaning)
            layout["view"].update(a)
        else:
            if  core.table_of_results:
                table = core.table_of_results
            else:
                table = self.show_similar_words(core=core)
            layout["view"].update(Padding(table,pad =(0,10),expand=True))
        from rich.spinner import Spinner  
        from app_state import DictionaryState  
        BORDER_STYLES ={
            DictionaryState.FIND: "blue",
            DictionaryState.SYNONYM: "plum2",
            DictionaryState.RHYMING_WORDS: "sky_blue1",

        }
        Subtitles = {
            DictionaryState.FIND: "Definition",
            DictionaryState.SYNONYM: "Synonyms",
            DictionaryState.RHYMING_WORDS: "Rhymes",
        }
        color = BORDER_STYLES.get(core.dictionary_state, "bold blue")
        subtitle = Subtitles.get(core.dictionary_state, "Dictionary")
        panel = Padding(Panel(self.format_text(core),border_style=color,subtitle=subtitle,subtitle_align="left"),pad =(0,20))
        layout["main"].update(panel)
        layout["suggestion"].update("")
        #layout["suggestion"].update(Padding(f"[dim {color}]{self.edit_suggestion(core)}[/dim {color}]",pad =(0,20),expand=True))
        return layout
    def show_similar_words(self, core: Core):
        """Updates layout to present a list of similar words in search"""
        split_entry_text = core.current_entry_text.split(" ")
        last_word = split_entry_text[-1] or (
            split_entry_text[-2] if len(split_entry_text) > 1 else ""
        )

        table = Table(expand=True, show_edge=False)
        table.add_column()

        # Get similar words using the dictionary service
        matches = DictionaryService.find_similar_words(
            last_word, 
            max_results=core.max_displayed_similar_words
        )

        for index, key in enumerate(matches[:core.max_displayed_similar_words]):
            if index == 0 and key == last_word:
                table.add_row(f"[bold blue]> {key}[/bold blue]", style=Style(color="blue"))
            else:
                table.add_row(key)
        return table
    def get_word_of_the_day(self):
        """Returns a random word from the lexicon"""
        return DictionaryService.get_word_of_the_day()
    def contains_primary_key(self,core:Core):
        """checks entry box for primary key 
        Returns:
            bool: True if present 
        """
        split_entry_text = core.current_entry_text.split(" ")
        for i in split_entry_text:
            if i in self.core.PRIMARY_KEY_WORD_MAPPING:
                return True
        return False