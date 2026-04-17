import re
import os

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text
from keybert import KeyBERT

kw_model = None

def load_keyword_model():
    return KeyBERT("all-MiniLM-L6-v2")


def extract_keywords(chunks, top_n=5):

    global kw_model
    if kw_model is None:
        try:
            kw_model = load_keyword_model()
        except Exception as e:
            print("Keyword model unavailable:", e)
            return [
                {**chunk, "keywords": []}
                for chunk in chunks
            ]

    results = []

    for chunk in chunks:

        if len(chunk["text"].split()) < 20:
            keyword_list = []

        else:
            cleaned_text = re.sub(r'\b\d+\b', '', chunk["text"])
            cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

            try:
                keywords = kw_model.extract_keywords(
                    cleaned_text,
                    keyphrase_ngram_range=(1,2),
                    stop_words="english",
                    use_maxsum=True,
                    nr_candidates=20,
                    top_n=top_n
                )
                keyword_list = [k[0] for k in keywords]
                keyword_list = list(dict.fromkeys(keyword_list))
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