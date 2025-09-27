"""Dictionary Services Module

This module provides dictionary-related services including:
- JSON data loading
- Word lookup and search functionality
- Similar word matching using fuzzy search
- Word of the day functionality
- Dictionary data management
"""
from pathlib import Path
import json
import random
from typing import Dict, List, Tuple, Optional
from rapidfuzz import process

import gzip

class DictionaryService:
    """Static service class for handling all dictionary-related operations"""
    
    # Class variables for data storage
    _lexicon: Optional[Dict] = None
    # Base path to the pyDictionary package
    BASE_PATH = Path(__file__).parent.parent

    _interface_guide: Optional[Dict] = None
    _dictionary_path: Path = BASE_PATH / "data" / "dictionary.json"
    _interface_guide_path: Path = BASE_PATH / "data" / "interface_guide.json"
    _suggestions: Optional[Dict] = None
    _interface_guide: Optional[Dict] = None

    _initialized: bool = False
    
    @classmethod
    def initialize(cls, dictionary_path: str = "data/dictionary.json", 
                   interface_guide_path: str = "data/interface_guide.json") -> None:
        """Initialize the dictionary service with data paths
        
        Args:
            dictionary_path (str): Path to the main dictionary JSON file
            interface_guide_path (str): Path to the interface guide JSON file
        """
        # Class variables for data storage
        _lexicon: Optional[Dict] = None
        # Base path to the pyDictionary package
        BASE_PATH = Path(__file__).parent.parent

        cls._dictionary_path: Path = BASE_PATH / "data" / "dictionary.json.gz"
        cls._interface_guide_path: Path = BASE_PATH / "data" / "interface_guide.json"


        _initialized: bool = False
    
        cls._load_all_data()
        cls._initialized = True
    @classmethod

    def load_lexicon_from_gz(cls,path) -> None:
        """Load lexicon data from a gzipped JSON file"""
        with gzip.open(path, "rt", encoding="utf-8") as f:
            dictionary_data = json.load(f)

        print("Loaded entries:", len(dictionary_data))
        return dictionary_data

    @classmethod
    def _load_all_data(cls) -> None:
        """Load all dictionary data from JSON files"""
        cls._lexicon = cls.load_lexicon_from_gz(cls._dictionary_path)
        cls._interface_guide = cls.load_json(cls._interface_guide_path)
        cls._suggestions = cls._interface_guide.get("SUGGESTIONS", {}) if cls._interface_guide else {}
    
    @classmethod
    def _ensure_initialized(cls) -> None:
        """Ensure the service is initialized with default paths if not already"""
        if not cls._initialized:
            cls.initialize()
    
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
    
    @classmethod
    def lexicon(cls) -> Dict:
        """Get the loaded lexicon dictionary"""
        cls._ensure_initialized()
        return cls._lexicon or {}
    
    @classmethod
    def suggestions(cls) -> Dict:
        """Get the suggestions dictionary"""
        cls._ensure_initialized()
        return cls._suggestions or {}
    
    @classmethod
    def find_word_definition(cls, word_to_find: str) -> Tuple[Optional[str], Optional[str]]:
        """Find word definition in dictionary
        
        Args:
            word_to_find (str): The word to search for
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (word, definition) if found, (None, None) if not found
        """
        cls._ensure_initialized()
        if not cls._lexicon:
            return None, None
            
        for key, value in cls._lexicon.items():
            if key.lower() == word_to_find.lower():
                return key, value
        return None, None
    
    @classmethod
    def get_word_of_the_day(cls) -> Tuple[str, str]:
        """Get a random word from the lexicon as word of the day
        
        Returns:
            Tuple[str, str]: (word, meaning) pair
        """
        cls._ensure_initialized()
        if not cls._lexicon:
            return "dictionary", "A reference work containing words and their meanings"
            
        word = random.choice(list(cls._lexicon.keys()))
        meaning = cls._lexicon[word]
        return word, meaning
    
    @classmethod
    def find_similar_words(cls, partial_word: str, max_results: int = 6, score_cutoff: int = 50) -> List[str]:
        """Find words similar to the partial word using prefix matching and fuzzy search
        
        Args:
            partial_word (str): The partial word to match against
            max_results (int): Maximum number of results to return
            score_cutoff (int): Minimum similarity score for fuzzy matches
            
        Returns:
            List[str]: List of similar words
        """
        cls._ensure_initialized()
        if not cls._lexicon or not partial_word:
            return []
        
        matches = []
        
        # Try exact match first
        exact_match = cls._lexicon.get(partial_word)
        if exact_match:
            matches.append(partial_word)
        
        # Try prefix matches
        prefix_matches = [k for k in cls._lexicon if k.startswith(partial_word.lower())]
        # Remove exact match if already added
        if partial_word in prefix_matches and exact_match:
            prefix_matches.remove(partial_word)
        
        matches.extend(prefix_matches)
        
        # If not enough matches, use fuzzy search
        if len(matches) < max_results:
            remaining_slots = max_results - len(matches)
            fuzzy_matches = process.extract(
                partial_word,
                cls._lexicon.keys(),
                limit=remaining_slots,
                score_cutoff=score_cutoff
            )
            # Extract just the words, not the scores
            fuzzy_words = [match[0] for match in fuzzy_matches]
            # Remove duplicates that might already be in matches
            fuzzy_words = [word for word in fuzzy_words if word not in matches]
            matches.extend(fuzzy_words)
        
        return matches[:max_results]
    
    @classmethod
    def get_word_count(cls) -> int:
        """Get the total number of words in the dictionary
        
        Returns:
            int: Number of words in the lexicon
        """
        cls._ensure_initialized()
        return len(cls._lexicon) if cls._lexicon else 0
    
    @classmethod
    def word_exists(cls, word: str) -> bool:
        """Check if a word exists in the dictionary
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if word exists, False otherwise
        """
        cls._ensure_initialized()
        if not cls._lexicon:
            return False
        return word.lower() in [k.lower() for k in cls._lexicon.keys()]
    
    @classmethod
    def get_suggestion(cls, state_value: str) -> str:
        """Get suggestion text for a given state
        
        Args:
            state_value (str): The state value to get suggestion for
            
        Returns:
            str: Suggestion text
        """
        cls._ensure_initialized()
        return cls._suggestions.get(state_value, "Enter a command")
    
    @classmethod
    def reload_data(cls) -> None:
        """Reload all dictionary data from files"""
        cls._load_all_data()
    @classmethod
    def get_random_meanings(cls, count: int = 3) -> List[Tuple[str, str]]:
        """Get a list of random (word, meaning) pairs from the lexicon
        
        Args:
            count (int): Number of random pairs to return   
        Returns:
            List[Tuple[str, str]]: List of (word, meaning) pairs
        """
        cls._ensure_initialized()
        if not cls._lexicon:
            return []
        
        # More memory efficient for large dictionaries
        keys = list(cls._lexicon.keys())
        selected_keys = random.sample(keys, min(count, len(keys)))
        return [cls._lexicon[key] for key in selected_keys]