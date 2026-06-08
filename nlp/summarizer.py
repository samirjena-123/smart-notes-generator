from transformers import pipeline
import os
import re
import streamlit as st

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text


@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        tokenizer="sshleifer/distilbart-cnn-12-6",
        device=-1
    )


def get_summarizer():
    try:
        return load_summarizer()
    except Exception as e:
        print("Summarizer failed to load:", e)
        return None


def generate_notes(chunks):
    if not chunks:
        return []

    model = get_summarizer()

    notes = []

    for chunk in chunks:

        # Short chunk — pass through directly
        if len(chunk["text"].split()) < 30:
            notes.append({
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "notes": [chunk["text"]],
                "heading": chunk.get("heading", "")
            })
            continue

        input_text = " ".join(chunk["text"].split()[:250])

        # ensure max_length always exceeds min_length
        min_len = 10
        max_len = max(min_len + 5, min(150, len(input_text.split()) // 2 + 30))

        # wrap summarizer call in try/except
        if model is None:
            notes.append({
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "notes": [chunk["text"]],
                "heading": chunk.get("heading", "")
            })
            continue

        try:
            summary = model(
                input_text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False,
                truncation=True
            )[0]["summary_text"]

        except Exception as e:
            print(f"Summarization failed for chunk {chunk['chunk_id']}:", e)
            notes.append({
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "notes": [chunk["text"]],
                "heading": chunk.get("heading", "")
            })
            continue

        # Rejoin broken decimals before splitting
        summary = re.sub(r'(\d)\s*\n\s*(\d)', r'\1.\2', summary)
        bullet_points = re.split(r'(?<=[.!?])\s+',summary)
        bullet_points = [
            bp.strip() for bp in bullet_points
            if 5 <= len(bp.split()) <= 25
        ]

        # Deduplicate
        seen = set()
        unique_points = []

        for bp in bullet_points:
            key = " ".join(bp.lower().split())
            if key not in seen:
                seen.add(key)
                unique_points.append(bp)

        bullet_points = unique_points

        if not bullet_points:
            cleaned_summary = summary.strip()
            bullet_points = [cleaned_summary] if cleaned_summary else [chunk["text"]]

        notes.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "notes": bullet_points,
            "heading": chunk.get("heading", "")
        })

    return notes


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    documents = load_document(sample_file)
    chunks = chunk_text(documents)
    notes = generate_notes(chunks)

    print(f"Total chunks: {len(chunks)}")
    print(f"Total notes objects: {len(notes)}")
    print()
    for n in notes:
        print(f"Chunk {n['chunk_id']} | Page {n['page']} | {len(n['notes'])} bullets")
        for b in n['notes']:
            print(f"   • {b}")
        print()