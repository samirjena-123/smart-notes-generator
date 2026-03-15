import re

def is_heading(text):
    text = text.strip()

    if len(text.split()) > 8:
        return False

    if text.isupper():
        return True

    if text.istitle():
        return True

    keywords = ["diversity", "ecosystem", "community", "conservation"]
    if any(k in text.lower() for k in keywords) and len(text.split()) <= 6:
        return True

    return False


def organize_notes(notes_data):

    organized = {}
    current_topic = "GENERAL"

    for item in notes_data:
        page = item["page"]

        for note in item["notes"]:

            # detect headings
            if is_heading(note):
                current_topic = note.upper()
                organized[current_topic] = []
                continue

            if current_topic not in organized:
                organized[current_topic] = []

            organized[current_topic].append(note)

    return organized

if __name__ == "__main__":

    from utils.document_loader import load_document
    from nlp.text_chunker import chunk_text
    from nlp.summarizer import generate_notes
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    docs = load_document(sample_file)
    chunks = chunk_text(docs)
    notes = generate_notes(chunks)

    organized = organize_notes(notes)

    for topic, points in organized.items():
        print("\n", topic)
        for p in points:
            print(" •", p)