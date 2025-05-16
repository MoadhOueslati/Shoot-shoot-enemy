
def format_timer(seconds):
    sec = seconds % 60
    min =  seconds // 60
    return f"{min:02d}:{sec:02d}"

