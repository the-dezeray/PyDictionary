"""the core module"""
import json
from rapidfuzz import fuzz, process

from rich.table import Table
from rich.layout import Layout
from rich.layout import Layout
from rich.padding import Padding
from rich.style import Style
from rich.live import Live

class Core():
    """process keyboard inputs/commands and updating layout appearance""" 

    def __init__(self) -> None:
        self.PRIMARY_KEY_WORD_MAPPING = {
            "find":self.find,
            "dictionary":self.dictionary,
            "use-case":self.use_case,
            "help":self.help,
            "synonyms":self.synonyms
            }

        #Core Related
        self.current_entry_text :str= ""
        self.clayout  =None
        self.formated_entry_text :str = ""
        self.suggestion :str = "" 
        self.running :str = True
        self.split_entry_text= ""
        self.selected :int = 0
        self.max_displayed_similar_words :int = 6
        #Layout related 
        self.table :Table = Table()
        self.live : Live
        self.selected_function : function = self.find #default function
        self.command = self.find
        #JSON DEPENDANT
        self.SUGGESTIONS: dict = None 
        self.HELP_MESSAGES : dict = None 
        self.ERROR_MESSAGES:dict = None 
        self.LEXICON :dict = None
        
        self.load_all()  #initialize json dependant variables

    def load_all(self):
        """initialize json dependant varibles a value"""
        
        self.LEXICON = self.load_json("dictionary.json")
        interface_guide= self.load_json("interface_guide.json")
 
        self.SUGGESTIONS = interface_guide["SUGGESTIONS"]
        self.ERROR_MESSAGES =interface_guide["ERRORS"]
        self.HELP_MESSAGES = interface_guide["HELP"]
        
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
     
    def save_key(self,key):
        """handles keyboard input"""
        input_string :str= str(key)
        input_string = input_string.replace("'","")
        
        match input_string:
            case "Key.down":    
                self.selected += 1
            case "Key.up":
                self.selected -= 1
            case "Key.space":
                input_string = " "
            
            case "Key.backspace":
                input_string = ""
                self.current_entry_text =  self.current_entry_text[:-1]
            
            #RUN COMMAND
            case "Key.enter":
                if self.clayout.name == "SettingTab":
                    self.selected_function()
                    
                else:
                    self.run_command()
                    self.current_entry_text = ""
                    self.formated_entry_text = ""
            case "Key.esc":
               from customLayouts import SettingTab
               self.clayout = SettingTab(self)

            #default
            case _:
                pass

        if len(input_string) <2: #<- prevents execution of unmapped keys !dont touch
            self.current_entry_text += input_string
            self.split_entry_text = self.current_entry_text.split(" ")
            self.format_text()
            self.edit_suggestion()
            self.show_similar_words()  

        self.live.update(self.clayout.update())
    def show_similar_words(self):
        """updates layout to present a list of similar words in search"""
        last_word = self.split_entry_text[-1] or (
            self.split_entry_text[-2] if len(self.split_entry_text) > 1 else ""
        )

        self.table = Table(expand=True, show_edge=False)
        self.table.add_column()

        # Try prefix matches first
        word  = "";
        word = self.LEXICON.get(last_word, None)
        matches = [k for k in self.LEXICON if k.startswith(last_word)]
        if word:
            matches.insert(0, last_word)
        # If not enough matches, fuzzy search
        if len(matches) < self.max_displayed_similar_words:
            extra_matches = process.extract(
                last_word,
                self.LEXICON.keys(),
                limit=self.max_displayed_similar_words - len(matches),
                score_cutoff=50
            )
            extra = [match[0] for match in extra_matches]
            matches.extend(extra)


        for index, key in enumerate(matches[:self.max_displayed_similar_words]):
            if index == 0 and key == last_word:

                self.table.add_row(f"[bold blue]> {key}[/bold blue]", style=Style(color="blue"))
            else:
                self.table.add_row(key)

    def contains_primary_key(self):
        """checks entry box for primary key 
        Returns:
            bool: True if present 
        """
        for i in self.split_entry_text:
            if i in self.PRIMARY_KEY_WORD_MAPPING:
                return True
        return False

    def edit_suggestion(self):
        """updates the suggestion renderable-object as input is updated
        """
        if len(self.current_entry_text )< 1: # if entry is empty
            self.suggestion = "Enter a command" #default suggeestion
        if  not self.contains_primary_key():
            matching_words = [word for word in self.PRIMARY_KEY_WORD_MAPPING if word.startswith(self.split_entry_text[-1])]
            if len(matching_words) > 0:
                for key,value in self.SUGGESTIONS.items():
                    if matching_words[0] == key :
                        self.suggestion = value

    def format_text(self):
        """formats the current user-input to highlight primary keys tags and text"""
        string_list =self.current_entry_text.split(" ")
        for index ,i in enumerate(string_list):
            if i in self.PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[code ] "  + i.upper() + "[/code]"
            if i in self.PRIMARY_KEY_WORD_MAPPING:
                string_list[index] = "[blue] "  + i + ": [/blue]"
        self.formated_entry_text = " ".join(string_list)

    def run_command(self):
        """runs user command """
       
 
        self.command()
        


    def find(self):
        """finds word in dictinary and updates renderable to dispay result """
        found = False
        last_word =self.split_entry_text[-1]
        self.table =  Table(expand=True,show_edge=False)
        self.table.add_column()
            
        if last_word == "" and len(self.split_entry_text) > 1: 
            last_word=self.split_entry_text[-2]
        for key,value in self.LEXICON.items():
            if key.lower() == last_word.lower():
                    found = True
                    self.table.add_row(f"{key.upper()}")
                    value = value.replace(";","\n")         
                    self.table.add_row(f"{value}")
        
        if found == False: self.table.add_row(f"[grey] [green]{last_word}[/green] not found  \n [i] Word maybe existing but not present in the database[/i][/grey]")
  

    def dictionary():
        pass

    def synonyms():
        return 0
    def help():
        pass
    def use_case():
        pass        

    def getTable(self):
        """returns the current table object"""
        options = {
            "find": "Find the meaning of a word",
            "dictionary": "Open the dictionary",
            "synonyms": "Show synonyms for a word",
            "games": "Show games related to a word",
            "use-case": "Show use cases for a word",
   
        }
        table = Table.grid(expand=True)
        self.selected = self.selected % len(options)
        for index, (key, value) in enumerate(options.items()):
            if index == self.selected:
                self.selected_function = lambda: self.set_mode(key)    
                table.add_row(f"[bold blue]{key}[/bold blue]", style=Style(color="blue"))
            else:
                table.add_row(key)
        return table
    def set_mode(self,mode:str):
        """sets the current function to be executed when enter is pressed"""
        from customLayouts import SettingTab,DictionaryLayout
        self.command = self.find
        self.clayout = DictionaryLayout(self)
        self.table = Table()
        self.live.update(self.clayout.update())
    def get_word_of_the_day(self):
        """returns a random word from the lexicon"""
        import random
        word = random.choice(list(self.LEXICON.keys()))
        meaning = self.LEXICON[word]
        return word, meaning