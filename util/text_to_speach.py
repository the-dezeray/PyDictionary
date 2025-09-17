# Import the required module for text 
# to speech conversion
from gtts import gTTS

# Import pygame for playing the converted audio
import pygame

def text_to_speech(text, language='en', slow=False, filename="welcome.mp3"):
    """
    Convert text to speech and play the audio.
    
    Args:
        text (str): The text to convert to speech
        language (str): Language code (default: 'en')
        slow (bool): Whether to speak slowly (default: False)
        filename (str): Name of the mp3 file to save (default: "welcome.mp3")
    """
    # Passing the text and language to the engine
    myobj = gTTS(text=text, lang=language, slow=slow)
    
    # Saving the converted audio in a mp3 file
    myobj.save(filename)
    
    # Initialize the mixer module
    pygame.mixer.init()
    
    # Load the mp3 file
    pygame.mixer.music.load(filename)
    
    # Play the loaded mp3 file
    pygame.mixer.music.play()
    
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

# Example usage:
# text_to_speech('Welcome to geeksforgeeks!')