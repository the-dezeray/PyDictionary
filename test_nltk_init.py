#!/usr/bin/env python3
"""Test script for the first_init function"""

import sys
import os
import time

# Add the src directory to the path so we can import richword modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from richword.util.nltk_handler import first_init, get_synonyms, get_rhyming_words

def test_nltk_initialization():
    """Test the NLTK initialization and functionality"""
    
    print("Testing NLTK initialization...")
    
    # Initialize NLTK
    init_thread = first_init()
    
    print("Waiting for initialization to complete...")
    
    # Wait a moment for initialization
    time.sleep(2)
    
    # Test basic functionality
    print("\nTesting synonyms for 'happy':")
    synonyms = get_synonyms("happy")
    print(f"Found {len(synonyms)} synonyms: {synonyms[:5]}")  # Show first 5
    
    print("\nTesting rhyming words for 'cat':")
    rhymes = get_rhyming_words("cat")
    print(f"Found {len(rhymes)} rhyming words: {rhymes[:5]}")  # Show first 5
    
    # Clean up
    if init_thread.is_alive():
        init_thread.join(timeout=5.0)
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_nltk_initialization()