from nltk.corpus import wordnet
import requests
import json

# Make sure you download WordNet once (can be cached offline)
import nltk
nltk.download('wordnet')


def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)


def get_rhyming_words(word):
    """Get words that rhyme with the given word using phonetic similarity"""
    rhymes = set()
    
    # Get all words from WordNet
    all_words = set()
    for synset in wordnet.all_synsets():
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


