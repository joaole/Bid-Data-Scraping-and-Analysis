import unidecode

def remove_special_characters(text):
    if isinstance(text, str):
        return unidecode.unidecode(text.lower())
    return text
