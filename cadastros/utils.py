from unidecode import unidecode

def true_or_false(text : str) -> bool :
    if text.lower() == 'true':
        return True
    return False

def clean_text(text: str) -> str :
    return unidecode(text).strip().upper()
        