import requests
import pygame
import io

def play_pronunciation(word: str):
    """
    Fetches pronunciation audio for a given word from the Free Dictionary API
    and plays it using pygame.

    Args:
        word (str): The word to look up.
    """
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    audio_url = None

    print(f"\nSearching for pronunciation of '{word}'...")

    try:
        # 1. Make a request to the dictionary API
        response = requests.get(api_url, timeout=10)

        # Handle word not found (404) or other HTTP errors
        if response.status_code == 404:
            print(f"Sorry, couldn't find the word '{word}'. Please check the spelling.")
            return
        elif response.status_code != 200:
            print(f"Error fetching data: Received status code {response.status_code}")
            return

        # 2. Parse the JSON response to find the audio URL
        data = response.json()
        for entry in data:
            if 'phonetics' in entry:
                for phonetic in entry['phonetics']:
                    # Find the first phonetic entry that has an audio link
                    if 'audio' in phonetic and phonetic['audio']:
                        audio_url = phonetic['audio']
                        break
            if audio_url:
                break
        
        if not audio_url:
            print(f"Sorry, no pronunciation audio was found for '{word}'.")
            return

        # The API sometimes returns URLs starting with "//", which need "https:"
        if audio_url.startswith('//'):
            audio_url = 'https:' + audio_url

        print(f"Found audio. Downloading and playing...")

        # 3. Download the audio file
        audio_response = requests.get(audio_url, timeout=10)
        if audio_response.status_code != 200:
            print("Failed to download the audio file.")
            return
            
        # 4. Play the audio using pygame
        # Use io.BytesIO to treat the downloaded audio content as a file
        audio_file = io.BytesIO(audio_response.content)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("Playback finished.")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Check for dependencies and guide the user if they are missing.
    try:
        import requests
        import pygame
    except ImportError:
        print("\n---")
        print("IMPORTANT: This script requires 'requests' and 'pygame'.")
        print("Please install them by opening your terminal or command prompt and running:")
        print("pip install requests pygame")
        print("---")
        exit()

    print("╔════════════════════════════════╗")
    print("║      Pronunciation Player      ║")
    print("╚════════════════════════════════╝")
    
    while True:
        # Get input from the user in a loop
        word_input = input("\nEnter a word to pronounce (or type 'quit' to exit): ").strip()

        if word_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if word_input:
            play_pronunciation(word_input)
        else:
            print("Please enter a word.")
