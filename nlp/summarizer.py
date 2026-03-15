from transformers import pipeline
import os
import re

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text


# smaller and faster model
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small",
    device=-1
)


def generate_notes(chunks):
    notes = []

    for chunk in chunks:

        if len(chunk["text"].split()) < 40:
            notes.append({
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "notes": [chunk["text"]]
            })
            continue

        text = "summarize the following text into concise bullet-point study notes: " + chunk["text"]

        summary = summarizer(
            text,
            max_length=min(80, len(text.split()) // 2 + 10),
            min_length=10,
            do_sample=False
        )[0]["summary_text"]

        bullet_points = re.split(r'\.\s+', summary)
        bullet_points = [bp.strip() for bp in bullet_points if len(bp.strip()) > 10]

        seen = set()
        bullet_points = [x for x in bullet_points if not (x in seen or seen.add(x))]

        if not bullet_points:
            bullet_points = [summary]

        notes.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "notes": bullet_points
        })

    return notes


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    documents = load_document(sample_file)

    chunks = chunk_text(documents)

    notes = generate_notes(chunks)

    for n in notes[:3]:
        print(n)