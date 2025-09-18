from renderers.dictionary_services import DictionaryService

# Initialize the dictionary service
_dictionary_service = DictionaryService()

# Export commonly used data for backward compatibility
LEXICON = _dictionary_service.lexicon
SUGGESTIONS = _dictionary_service.suggestions

# Export the service instance for direct use
dictionary_service = _dictionary_service