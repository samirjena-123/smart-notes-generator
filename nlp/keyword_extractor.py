import re
import os

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text
from keybert import KeyBERT

_kw_model = None


def get_keyword_model():
    global _kw_model
    if _kw_model is None:
        try:
            _kw_model = KeyBERT("all-MiniLM-L6-v2")
        except Exception as e:
            print("Keyword model unavailable:", e)
            _kw_model = None
    return _kw_model


def extract_keywords(chunks, top_n=5, min_words=20):

    model = get_keyword_model()

    if model is None:
        return [
            {**chunk, "keywords": []}
            for chunk in chunks
        ]

    results = []

    for chunk in chunks:

        if len(chunk["text"].split()) < min_words:
            keyword_list = []

        else:
            cleaned_text = re.sub(r'\b\d+\b', '', chunk["text"])
            cleaned_text = re.sub(r'[^\w\s\-]', ' ', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            if not cleaned_text:
                keyword_list = []
            else:

                try:
                    word_count = len(cleaned_text.split())
                    nr_candidates = min(max(20, word_count // 5), 50)

                    keywords = model.extract_keywords(
                        cleaned_text,
                        keyphrase_ngram_range=(1, 2),
                        stop_words="english",
                        use_maxsum=True,
                        nr_candidates=nr_candidates,
                        top_n=top_n
                    )

                    keyword_list = [
                        {"keyword": k[0], "score": round(k[1], 4)}
                        for k in keywords
                    ]
                    # Deduplicate by keyword text
                    seen = set()
                    deduped = []
                    for k in keyword_list:
                        key = " ".join(k["keyword"].lower().split())

                        if key not in seen:
                            seen.add(key)
                            deduped.append(k)
                    keyword_list = deduped

                except Exception as e:
                    print("Keyword extraction failed:", e)
                    keyword_list = []

        results.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "keywords": keyword_list
        })

    return results


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    documents = load_document(sample_file)
    chunks = chunk_text(documents)
    keyword_results = extract_keywords(chunks)

    for r in keyword_results[:5]:
        print(r)