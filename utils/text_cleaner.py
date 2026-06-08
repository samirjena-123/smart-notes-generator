import re


def clean_text(text):

    if not isinstance(text, str):
        return ""
    
    
    # Remove ALL invisible/control characters except normal whitespace
    text = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad\u180e\u2028\u2029]', '', text)    # Protect decimal numbers
    text = re.sub(r'(\d)\s*\.\s*(\d)', r'\1DECIMAL\2', text)
    # normalize unicode spaces and artifacts
    text = text.replace('\xa0', ' ')       # non-breaking space
    text = text.replace('\u200b', '')      # zero-width space
    text = text.replace('\ufeff', '')      # BOM character
    text = text.replace('\u00ad', '')      # soft hyphen
    text = text.replace('\u2019', "'")     # curly apostrophe
    text = text.replace('\u201c', '"')     # left double quote
    text = text.replace('\u201d', '"')     # right double quote

    # only remove bullet symbols at line start, not mid-word hyphens
    text = re.sub(r'(?m)^[•▪●◦–]\s*', '', text)  # line start

    text = re.sub(r'\n{3,}', '\n\n', text)

    # collapse spaces and tabs
    text = re.sub(r'[ \t]+', ' ', text)

    # Restore decimal numbers
    text = text.replace('DECIMAL', '.')

    return text.strip()