import re

def clean_text(text):
    # normalize unicode spaces
    text = text.replace('\xa0', ' ')

    # remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # collapse excessive spaces but keep newlines
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()