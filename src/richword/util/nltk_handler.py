import requests
import json
import os
import threading

# Global variables for threaded initialization
_nltk_initialized = False
_nltk_init_lock = threading.Lock()
_wordnet = None
_nltk = None

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate to the data directory (assuming it's at src/richword/data)
data_dir = os.path.join(os.path.dirname(current_dir), "data", "nltk_data")


def _check_wordnet_exists():
    """Check if wordnet data exists by looking for the wordnet zip or directory"""
    wordnet_zip_path = os.path.join(data_dir, "corpora", "wordnet.zip")
    wordnet_dir_path = os.path.join(data_dir, "corpora", "wordnet")
    
    return os.path.exists(wordnet_zip_path) or os.path.exists(wordnet_dir_path)


def _download_wordnet():
    """Download wordnet data if it doesn't exist"""
    import nltk
    
    if not _check_wordnet_exists():
        # Create the data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        print("Downloading WordNet data...")
        nltk.download("wordnet", download_dir=data_dir)
        print("WordNet data downloaded successfully!")


def _initialize_nltk_threaded():
    """Initialize NLTK in a separate thread"""
    global _nltk_initialized, _wordnet, _nltk
    
    with _nltk_init_lock:
        if not _nltk_initialized:
            print("Initializing NLTK...")
            import nltk
            from nltk.corpus import wordnet
            
            _nltk = nltk
            _wordnet = wordnet
            
            # Add the data directory to NLTK's data path
            if data_dir not in nltk.data.path:
                nltk.data.path.append(data_dir)
            
            _nltk_initialized = True
            print("NLTK initialization complete!")


def first_init():
    """
    Initialize NLTK and WordNet data before the program runs.
    Downloads WordNet if not present and imports NLTK in a separate thread.
    """
    # First, do a quick import of nltk to check if wordnet exists
    import nltk
    
    # Add the data directory to NLTK's data path
    if data_dir not in nltk.data.path:
        nltk.data.path.append(data_dir)
    
    # Check if wordnet data exists, download if not
    try:
        nltk.data.find("corpora/wordnet")
        print("WordNet data found!")
    except LookupError:
        _download_wordnet()
    
    # Start NLTK initialization in a separate thread
    init_thread = threading.Thread(target=_initialize_nltk_threaded, daemon=True)
    init_thread.start()
    
    return init_thread


def _wait_for_nltk_init():
    """Wait for NLTK initialization to complete"""
    while not _nltk_initialized:
        threading.Event().wait(0.1)  # Small delay to prevent busy waiting


def get_synonyms(word):
    """Get synonyms for a word using WordNet"""
    _wait_for_nltk_init()  # Ensure NLTK is initialized
    
    if _wordnet is None:
        return []
    
    synonyms = set()
    for synset in _wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)


def get_rhyming_words(word):
    """Get words that rhyme with the given word using phonetic similarity"""
    _wait_for_nltk_init()  # Ensure NLTK is initialized
    
    if _wordnet is None:
        return []
    
    rhymes = set()
    
    # Get all words from WordNet
    all_words = set()
    for synset in _wordnet.all_synsets():
        for lemma in synset.lemmas():
            all_words.add(lemma.name().lower())
    
    # Simple phonetic matching - look for words ending with similar sounds
    word = word.lower().strip()
    if len(word) < 2:
        return []
    
    # Get the ending sound patterns (last 2-3 characters)
    ending2 = word[-2:] if len(word) >= 2 else word
    ending3 = word[-3:] if len(word) >= 3 else word
    
    for w in all_words:
        if w == word or len(w) < 2:
            continue
        
        # Check if words end with similar sounds
        if (len(w) >= 2 and w[-2:] == ending2) or (len(w) >= 3 and w[-3:] == ending3):
            # Additional check to avoid too similar words (like plurals)
            if w != word and not w.startswith(word) and not word.startswith(w):
                rhymes.add(w.replace('_', ' '))
    
    # Limit results and sort them
    return sorted(list(rhymes))[:20]  # Return up to 20 rhyming words


def search_words_by_meaning(meaning_phrase):
    """Search for words that match a given meaning using Datamuse API"""
    try:
        # Datamuse API endpoint for "means like" searches
        url = "https://api.datamuse.com/words"
        params = {
            'ml': meaning_phrase,  # means like
            'max': 20  # limit results to 20 words
        }
        
        # Make the API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Parse JSON response
        data = response.json()
        
        if data:
            # Extract just the words from the response
            # Each item is a dict with 'word' and 'score' keys
            words = [item['word'] for item in data]
            return words
        else:
            return []
            
    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print(f"API request failed: {e}")
        return []
    except json.JSONDecodeError:
        # Handle invalid JSON response
        print("Invalid JSON response from API")
        return []
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        return []


