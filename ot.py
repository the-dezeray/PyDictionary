from core import Core
from rich.panel import Panel
def activate_voice(core):
    core.instruction = Panel("Voice Activated\n [cyan]|||||[/cyan]")
    word = core.current_word
    definition = core.current_definition
    if word and definition:
        from util.text_to_speach import text_to_speech
        text_to_speech(f"{word}. {definition}")