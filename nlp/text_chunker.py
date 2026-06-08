import os

from utils.document_loader import load_document


def chunk_text(documents, chunk_size=None, overlap=None):
    if not documents:
        return []

    # Auto-detect chunk size based on average document length
    if chunk_size is None:
        all_words = [len(doc["text"].split()) for doc in documents if doc.get("text", "").strip()]
        if all_words:
            avg_words = sum(all_words) / len(all_words)
            if avg_words < 100:
                chunk_size = 80        # short slides
            elif avg_words < 500:
                chunk_size = 200       # medium docs
            else:
                chunk_size = 350       # long reports
        else:
            chunk_size = 200

    if overlap is None:
        overlap = max(20, chunk_size // 6)

    # Validate
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        overlap = chunk_size // 4

    chunks = []
    chunk_id = 1

    for doc in documents:

        if not doc.get("text", "").strip():
            continue

        words = doc["text"].split()
        total_words = len(words)
        start = 0

        while start < total_words:

            end = min(start + chunk_size, total_words)
            chunk_words = words[start:end]

            # Skip if too small and not the only chunk
            if len(chunk_words) < 15 and chunks:
                chunks[-1]["text"] += " " + " ".join(chunk_words)
                break

            chunk_str = " ".join(chunk_words)

            chunks.append({
                "source": doc["source"],
                "page": doc["page"],
                "chunk_id": chunk_id,
                "text": chunk_str,
                "headings": doc.get("headings", []),
                "heading": doc.get("heading", "")
            })

            chunk_id += 1
            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    documents = load_document(sample_file)
    chunks = chunk_text(documents)

    print("\n=== DOCUMENTS COMING IN ===")
    for d in documents:
        print(f"Page {d['page']} | heading='{d.get('heading','')}' | {len(d['text'].split())} words")

    print(f"Total documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    for c in chunks:
        print(f"Chunk {c['chunk_id']} | Page {c['page']} | {len(c['text'].split())} words")

    