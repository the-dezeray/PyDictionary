from .core import Core
from rich.panel import Panel
from .util.text_to_speach import text_to_speech
def activate_voice(core:"Core"):
    core.instruction = Panel("Voice Activated\n [cyan]|||||[/cyan]")
    word = core.current_word
    definition = core.current_definition
    core.voice_activate = True
    if word and definition:

        text_to_speech(f"{word}")

