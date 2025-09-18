"""Dictionary Services Module

This module provides dictionary-related services including:
- JSON data loading
- Word lookup and search functionality
- Similar word matching using fuzzy search
- Word of the day functionality
- Dictionary data management
"""

import json
import random
from typing import Dict, List, Tuple, Optional
from rapidfuzz import process


class DictionaryService:
    """Service class for handling all dictionary-related operations"""
    
    def __init__(self, dictionary_path: str = "data/dictionary.json", 
                 interface_guide_path: str = "data/interface_guide.json"):
        """Initialize the dictionary service with data paths
        
        Args:
            dictionary_path (str): Path to the main dictionary JSON file
            interface_guide_path (str): Path to the interface guide JSON file
        """
        self.dictionary_path = dictionary_path
        self.interface_guide_path = interface_guide_path
        
        # Data storage
        self._lexicon: Optional[Dict] = None
        self._suggestions: Optional[Dict] = None
        self._interface_guide: Optional[Dict] = None
        
        # Load initial data
        self._load_all_data()
    
    def _load_all_data(self) -> None:
        """Load all dictionary data from JSON files"""
        self._lexicon = self.load_json(self.dictionary_path)
        self._interface_guide = self.load_json(self.interface_guide_path)
        self._suggestions = self._interface_guide.get("SUGGESTIONS", {})
    
    @staticmethod
    def load_json(file_path: str) -> Dict:
        """Load and return contents of a JSON file
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: File contents as dictionary
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(file_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print(f"Error: Could not find file {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file {file_path}: {e}")
            return {}
    
    @property
    def lexicon(self) -> Dict:
        """Get the loaded lexicon dictionary"""
        return self._lexicon or {}
    
    @property
    def suggestions(self) -> Dict:
        """Get the suggestions dictionary"""
        return self._suggestions or {}
    
    def find_word_definition(self, word_to_find: str) -> Tuple[Optional[str], Optional[str]]:
        """Find word definition in dictionary
        
        Args:
            word_to_find (str): The word to search for
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (word, definition) if found, (None, None) if not found
        """
        if not self._lexicon:
            return None, None
            
        for key, value in self._lexicon.items():
            if key.lower() == word_to_find.lower():
                return key, value
        return None, None
    
    def get_word_of_the_day(self) -> Tuple[str, str]:
        """Get a random word from the lexicon as word of the day
        
        Returns:
            Tuple[str, str]: (word, meaning) pair
        """
        if not self._lexicon:
            return "dictionary", "A reference work containing words and their meanings"
            
        word = random.choice(list(self._lexicon.keys()))
        meaning = self._lexicon[word]
        return word, meaning
    
    def find_similar_words(self, partial_word: str, max_results: int = 6, score_cutoff: int = 50) -> List[str]:
        """Find words similar to the partial word using prefix matching and fuzzy search
        
        Args:
            partial_word (str): The partial word to match against
            max_results (int): Maximum number of results to return
            score_cutoff (int): Minimum similarity score for fuzzy matches
            
        Returns:
            List[str]: List of similar words
        """
        if not self._lexicon or not partial_word:
            return []
        
        matches = []
        
        # Try exact match first
        exact_match = self._lexicon.get(partial_word)
        if exact_match:
            matches.append(partial_word)
        
        # Try prefix matches
        prefix_matches = [k for k in self._lexicon if k.startswith(partial_word.lower())]
        # Remove exact match if already added
        if partial_word in prefix_matches and exact_match:
            prefix_matches.remove(partial_word)
        
        matches.extend(prefix_matches)
        
        # If not enough matches, use fuzzy search
        if len(matches) < max_results:
            remaining_slots = max_results - len(matches)
            fuzzy_matches = process.extract(
                partial_word,
                self._lexicon.keys(),
                limit=remaining_slots,
                score_cutoff=score_cutoff
            )
            # Extract just the words, not the scores
            fuzzy_words = [match[0] for match in fuzzy_matches]
            # Remove duplicates that might already be in matches
            fuzzy_words = [word for word in fuzzy_words if word not in matches]
            matches.extend(fuzzy_words)
        
        return matches[:max_results]
    
    def get_word_count(self) -> int:
        """Get the total number of words in the dictionary
        
        Returns:
            int: Number of words in the lexicon
        """
        return len(self._lexicon) if self._lexicon else 0
    
    def word_exists(self, word: str) -> bool:
        """Check if a word exists in the dictionary
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if word exists, False otherwise
        """
        if not self._lexicon:
            return False
        return word.lower() in [k.lower() for k in self._lexicon.keys()]
    
    def get_suggestion(self, state_value: str) -> str:
        """Get suggestion text for a given state
        
        Args:
            state_value (str): The state value to get suggestion for
            
        Returns:
            str: Suggestion text
        """
        return self._suggestions.get(state_value, "Enter a command")
    
    def reload_data(self) -> None:
        """Reload all dictionary data from files"""
        self._load_all_data()
