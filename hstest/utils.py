

def normalize_line_endings(text: str) -> str:
    return text.replace('\r\n', '\n').replace('\r', '\n')
