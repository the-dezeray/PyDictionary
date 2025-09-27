def navigate(ui_state,direction:str):
    """navigate through menu options"""
    if direction == "up":
        ui_state.selected -= 1
    elif direction == "down":
        ui_state.selected += 1