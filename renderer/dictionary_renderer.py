from rich.layout import Layout
from art import text2art
from rich.panel import Panel
from rich.padding import Padding
from  nlayout import lll
from core import Core
from rich.table import Table
from rich.style import Style
from rapidfuzz import fuzz, process
from app_state import CustomLayout
import json
class DictionaryLayout(CustomLayout):
    def load_json(self,file_path:str):
        """returns file contents of a JSON-file 
    
        Args:
            file_path (str): string of the file path
        Returns:
            dict : file contents
        """
        with open(file_path,"r")as json_file:
            file_content : dict = json.load(json_file)
        return file_content
     
    def __init__(self,core):
        super().__init__(core)
        self.core = core
        self.name = "DictionaryLayout"
        self.f = 0
        interface_guide= self.load_json("interface_guide.json")
        self.PRIMARY_KEY_WORD_MAPPING = {
            "find":(),
            "dictionary":(),
            "use-case":(),
            "help":(),
            "synonyms":()
            }
        self.SUGGESTIONS = interface_guide["SUGGESTIONS"]
        self.LEXICON = self.load_json("dictionary.json")
        self.suggestion = "Enter a command"
    def format_text(self,core: Core):
        """formats the current user-input to highlight primary keys tags and text"""
        PRIMARY_KEY_WORD_MAPPING = {
            "find":(),
            "dictionary":(),
            "use-case":(),
            "help":(),
            "synonyms":()
            }
        
        string_list =core.current_entry_text.split(" ")
        for index ,i in enumerate(string_list):
            if i in PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[code ] "  + i.upper() + "[/code]"
            if i in PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[blue] "  + i + ": [/blue]"
        formated_entry_text = " ".join(string_list)
        return formated_entry_text
    def edit_suggestion(self,core:Core):
        """updates the suggestion renderable-object as input is updated
        """
        PRIMARY_KEY_WORD_MAPPING = {
            "find":(),
            "dictionary":(),
            "use-case":(),
            "help":(),
            "synonyms":()
            }
        split_entry_text = core.current_entry_text.split(" ")
        if len(core.current_entry_text )< 1: # if entry is empty
            self.suggestion = "Enter a command" #default suggeestion
        if  not self.contains_primary_key(core):
            matching_words = [word for word in PRIMARY_KEY_WORD_MAPPING if word.startswith(split_entry_text[-1])]
            if len(matching_words) > 0:
                for key,value in self.SUGGESTIONS.items():
                    if matching_words[0] == key :
                        self.suggestion = value
        return self.suggestion
    def update(self,core: Core):
 
        layout = lll()
        if core.key_count == 0:
         
            (word,meaning) = self.get_word_of_the_day()
            art = text2art(f"{word}",font="tarty4")
            from rich.align import Align
            layout["view"].update(Padding(pad=(0,10),renderable=Padding(Align(f"[green]{art}[/green] \n\n{meaning}",align="center"))))
        else:
            if  core.table_of_results:
                table = core.table_of_results
            else:
                table = self.show_similar_words(core=core)
            layout["view"].update(Padding(table,pad =(0,10),expand=True))
        layout["main"].update(Padding(Panel(self.format_text(core)),pad =(0,20)))
        layout["suggestion"].update(Padding(self.edit_suggestion(core),pad =(0,20),expand=True))
        return layout
    def show_similar_words(self,core:Core):
        """updates layout to present a list of similar words in search"""
        split_entry_text = core.current_entry_text.split(" ")
        last_word = split_entry_text[-1] or (
            split_entry_text[-2] if len(split_entry_text) > 1 else ""
        )

        table = Table(expand=True, show_edge=False)
        table.add_column()

        # Try prefix matches first
        word  = "";
        word = self.LEXICON.get(last_word, None)
        matches = [k for k in self.LEXICON if k.startswith(last_word)]
        if word:
            matches.insert(0, last_word)
        # If not enough matches, fuzzy search
        if len(matches) < core.max_displayed_similar_words:
            extra_matches = process.extract(
                last_word,
                self.LEXICON.keys(),
                limit=core.max_displayed_similar_words - len(matches),
                score_cutoff=50
            )
            extra = [match[0] for match in extra_matches]
            matches.extend(extra)


        for index, key in enumerate(matches[:core.max_displayed_similar_words]):
            if index == 0 and key == last_word:

                table.add_row(f"[bold blue]> {key}[/bold blue]", style=Style(color="blue"))
            else:
                table.add_row(key)
        return table
    def get_word_of_the_day(self):
        """returns a random word from the lexicon"""
        import random

        word = random.choice(list(self.LEXICON.keys()))
        meaning = self.LEXICON[word]
        return word, meaning
    def contains_primary_key(self,core:Core):
        """checks entry box for primary key 
        Returns:
            bool: True if present 
        """
        split_entry_text = core.current_entry_text.split(" ")
        for i in split_entry_text:
            if i in self.PRIMARY_KEY_WORD_MAPPING:
                return True
        return False