from .renderers.dictionary_services import DictionaryService

# Initialize the static dictionary service
DictionaryService.initialize()

# Export commonly used data for backward compatibility
LEXICON = DictionaryService.lexicon()
SUGGESTIONS = DictionaryService.suggestions()

# Export the service class for direct use
dictionary_service = DictionaryService