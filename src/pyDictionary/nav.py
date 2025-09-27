def navigate(core,direction:str):
    """navigate through menu options"""
    if direction == "up":
        core.selected -= 1
    elif direction == "down":
        core.selected += 1