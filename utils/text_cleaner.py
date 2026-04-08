import re

def clean_text(text):

    # normalize unicode spaces
    text = text.replace('\xa0', ' ')
    text = text.replace('\u200b', '')
    text = text.replace('\ufeff', '')

    # remove bullet symbols
    text = re.sub(r'[•▪●◦–-]\s*', '', text)

    # fix broken lines (join lines inside sentences)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # collapse spaces
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()