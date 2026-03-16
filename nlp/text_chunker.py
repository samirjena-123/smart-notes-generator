import os
from utils.document_loader import load_document

def chunk_text(documents, chunk_size=300, overlap=50):

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for doc in documents:

        if not doc["text"]:
            continue

        words = doc["text"].split()

        start = 0
        chunk_id = 1

        while start < len(words):

            end = start + chunk_size
            chunk_words = words[start:end]

            if len(chunk_words) < 20:
                break

            chunk_text = " ".join(chunk_words)

            chunks.append({
                "source": doc["source"],
                "page": doc["page"],
                "chunk_id": chunk_id,
                "text": chunk_text
            })

            chunk_id += 1
            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    documents = load_document(sample_file)

    chunks = chunk_text(documents)

    for c in chunks[:5]:
        print(c)