"""Text processing utilities for the richword application"""

import re


def count_words_in_definition(text):
    """Count words in definition text, ignoring Rich markup tags"""
    # Remove Rich markup tags like [bold], [/bold], [italic], etc.
    clean_text = re.sub(r'\[/?[a-zA-Z0-9\s]*\]', '', str(text))
    # Split by whitespace and count non-empty parts
    words = clean_text.split()
    return len([word for word in words if word.strip()])


def extract_last_word(entry_text: str) -> str:
    """Extract the last word from entry text, handling empty strings"""
    split_entry_text = entry_text.split(" ")
    last_word = split_entry_text[-1]
    
    if last_word == "" and len(split_entry_text) > 1:
        last_word = split_entry_text[-2]
    
    return last_word