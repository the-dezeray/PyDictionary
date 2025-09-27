import io
from gtts import gTTS
import pygame

def text_to_speech(text, language='en', slow=False):
    mp3_fp = io.BytesIO()
    gTTS(text=text, lang=language, slow=slow).write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, "mp3")  # load from memory
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    pygame.mixer.quit()
