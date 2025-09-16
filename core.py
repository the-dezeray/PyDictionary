"""the core module"""
import json
from rapidfuzz import fuzz, process
import re
from rich.table import Table
from rich.layout import Layout
from rich.layout import Layout
from rich.padding import Padding
from rich.style import Style
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
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
        self.word_limit :int = 50  # Maximum words before truncating definition
        self.show_full_definition :bool = False  # Flag for showing full definition
        self.last_found_definition :str = ""  # Store full definition for 'n' command
        self.last_found_word :str = ""  # Store the word for full definition display
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

    def count_words_in_definition(self, text):
        """Count words in definition text, ignoring Rich markup tags"""
        # Remove Rich markup tags like [bold], [/bold], [italic], etc.
        clean_text = re.sub(r'\[/?[a-zA-Z0-9\s]*\]', '', str(text))
        # Split by whitespace and count non-empty parts
        words = clean_text.split()
        return len([word for word in words if word.strip()])

    def truncate_definition(self, text, word_limit):
        """Truncate definition text to specified word limit while preserving Rich markup structure"""
        # Convert Text object to string if needed
        text_str = str(text) if hasattr(text, 'plain') else text
        
        # Remove Rich markup for word counting
        clean_text = re.sub(r'\[/?[a-zA-Z0-9\s]*\]', '', text_str)
        words = clean_text.split()
        
        if len(words) <= word_limit:
            return text, False  # No truncation needed
        
        # Find the position to truncate in the original text
        truncated_words = words[:word_limit]
        truncated_clean = ' '.join(truncated_words)
        
        # Simple approach: find approximate position in original text
        # This is a basic implementation that may need refinement for complex markup
        words_so_far = 0
        result = ""
        i = 0
        
        while i < len(text_str) and words_so_far < word_limit:
            char = text_str[i]
            result += char
            
            # Check if we've completed a word (not inside markup)
            if char == ' ' and not self._inside_markup(text_str, i):
                words_so_far += 1
            
            i += 1
        
        return result + "...", True  # Return truncated text and truncation flag
    
    def _inside_markup(self, text, position):
        """Helper method to check if position is inside Rich markup tags"""
        # Look backwards for the last [ or ]
        last_bracket = -1
        for i in range(position - 1, -1, -1):
            if text[i] in ['[', ']']:
                last_bracket = i
                ##
                break
        
        if last_bracket == -1:
            return False
        
        return text[last_bracket] == '['

    def run_command(self):
        """runs user command """
        
        # Check if user typed 'n' to show full definition
        if self.current_entry_text.strip().lower() == 'n':
            self.show_full_definition_method()
        else:
            self.show_full_definition = False  # Reset full definition flag
            self.command()

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
        

    def find(self):
            """finds word in dictinary and updates renderable to dispay result """
            
            found = False
            last_word = self.split_entry_text[-1]
            self.table = Table(expand=True, show_edge=False)
            self.table.add_column()
                
            if last_word == "" and len(self.split_entry_text) > 1: 
                last_word = self.split_entry_text[-2]
            
            for key, value in self.LEXICON.items():
                if key.lower() == last_word.lower():
                    found = True
                    
                    # Style scientific names (e.g., "(Salvelinus malma)")
                    processed_def = re.sub(
                        r'(\([A-Z][a-z]+ [a-z]+\))',
                        r'[italic]\1[/italic]',
                        value
                    )

                    # Style usage tags (e.g., "[Obs.]")
                    processed_def = re.sub(
                        r'(\[[A-Za-z\.\s,]+\])',
                        r'[dim italic]\1[/dim italic]',
                        processed_def
                    )
                    
                    # Style special notes (e.g., "Note: ...")
                    processed_def = re.sub(
                        r'Note: (.*?)(?=\s\d\.\s|$)',
                        r'\n    [bold]Note[/bold]: [dim]\1[/dim]',
                        processed_def,
                        flags=re.DOTALL
                    )

                    # Style quotes and attributions (e.g., "Sentence. Author.")
                    processed_def = re.sub(
                        r'([A-Z][^."]*?\.)\s+([A-Z][a-z]+\.)',
                        r'\n    [italic]" \1"[/italic]\n    — \2',
                        processed_def
                    )

                    # Style alternative names (e.g., "-- called also ...")
                    processed_def = re.sub(
                        r'--\s*called also\s*(.*)',
                        lambda m: f"\nCalled also: [bold]{m.group(1).strip('.')}[/bold]",
                        processed_def
                    )
                    
                    # Split definitions into numbered parts
                    parts = re.split(r'\s(?=\d\.\s)', processed_def)
                    
                    # If there are numbered parts, format them
                    if len(parts) > 1 or value.strip().startswith('1.'):
                        formatted_text = Text()
                        for i, part in enumerate(parts):
                            part = part.strip()
                            # Find the number and the text
                            match = re.match(r'(\d\.)\s*(.*)', part, re.DOTALL)
                            if match:
                                num, text = match.groups()
                                formatted_text.append(f"\n[bold cyan]{num}[/bold cyan] ")
                                formatted_text.append(text.strip())
                            else: # Handles the text before the first '1.' if any
                                formatted_text.append(part.strip())
                        final_text = formatted_text
                    else:
                        # Handle definitions without numbers
                        final_text = processed_def.strip()

                    # Store full definition for potential 'n' command
                    self.last_found_definition = str(final_text)
                    self.last_found_word = key
                    
                    # Check if definition needs truncation
                    word_count = self.count_words_in_definition(final_text)
                    if word_count > self.word_limit and not self.show_full_definition:
                        truncated_text, was_truncated = self.truncate_definition(final_text, self.word_limit)
                        if was_truncated:
                            display_text = f"{truncated_text}\n\n[dim yellow]Definition truncated ({word_count} words). Type 'n' for full definition.[/dim yellow]"
                        else:
                            display_text = final_text
                    else:
                        display_text = final_text

                    panel = Panel(
                        display_text,
                        title=f"[bold yellow]{key}[/bold yellow]",
                        title_align="left",
                        expand=True
                    )        
                    self.table.add_row(panel)

            if found == False: 
                self.table.add_row(f"[grey] [green]{last_word}[/green] not found  \n [i] Word maybe existing but not present in the database[/i][/grey]")

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