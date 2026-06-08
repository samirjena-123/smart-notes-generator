def organize_notes(notes_data):

    organized = {"GENERAL": []}

    for item in notes_data:

        current_topic = "GENERAL"

        section_heading = str(item.get("heading", "")).strip()
        if section_heading:
            current_topic = section_heading.strip()
            organized.setdefault(current_topic, [])

        for note in item.get("notes", []):

            if not note.strip():
                continue

            # handle [Title] tags from ppt_parser
            if note.startswith("[Title]"):
                current_topic = note.replace("[Title]", "").strip().upper()
                organized.setdefault(current_topic, [])
                continue

            # deduplicate notes under same topic
            existing = organized.setdefault(current_topic, [])
            normalized_existing = {
                " ".join(x.lower().split())
                for x in existing
            }

            normalized_note = " ".join(note.lower().split())

            if normalized_note not in normalized_existing:
                existing.append(note)

    return {k: v for k, v in organized.items() if v}


if __name__ == "__main__":

    from utils.document_loader import load_document
    from nlp.text_chunker import chunk_text
    from nlp.summarizer import generate_notes
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    docs = load_document(sample_file)
    chunks = chunk_text(docs)
    notes = generate_notes(chunks)

    organized = organize_notes(notes)

    print("\n=== HEADINGS IN NOTES ===")
    for n in notes:
        print(f"Chunk {n['chunk_id']} | heading='{n.get('heading', '')}'")

    for topic, points in organized.items():
        print("\n", topic)
        for p in points:
            print(" •", p)