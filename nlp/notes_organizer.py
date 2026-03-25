def is_heading(text):

    text = text.strip()
    words = text.split()

    if len(words) == 0:
        return False

    if len(words) > 8:
        return False

    if text.endswith("."):
        return False

    if text.isupper():
        return True

    if text.istitle() and len(words) <= 5 and not text.isdigit():
        return True

    return False


def organize_notes(notes_data):

    organized = {"GENERAL": []}
    current_topic = "GENERAL"

    for item in notes_data:

        for note in item["notes"]:

            if not note.strip():
                continue

            if is_heading(note):
                current_topic = " ".join(note.strip().split()).upper()
                organized.setdefault(current_topic, [])
                continue

            organized.setdefault(current_topic, []).append(note)

    return {k: v for k, v in organized.items() if v}

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