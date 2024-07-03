import unidecode

def remove_special_characters(texts):
    return [unidecode.unidecode(str(text).lower()) for text in texts]

