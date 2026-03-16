import os

from extraction.pdf_parser import extract_text_from_pdf
from extraction.ppt_parser import extract_text_from_ppt
from extraction.docx_parser import extract_text_from_docx

from utils.text_cleaner import clean_text


def load_document(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".pdf":
        pages = extract_text_from_pdf(file_path)

    elif file_ext == ".pptx":
        pages = extract_text_from_ppt(file_path)

    elif file_ext == ".docx":
        pages = extract_text_from_docx(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

    if not pages:
        print("Warning: No content extracted from document.")
        return []

    documents = []

    for item in pages:

        cleaned_text = clean_text(item["text"])

        if not cleaned_text:
            continue

        page_number = item.get("page") or item.get("slide") or 1

        documents.append({
            "source": os.path.basename(file_path),
            "page": page_number,
            "text": cleaned_text
        })

    return documents


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    docs = load_document(sample_file)

    for d in docs[:3]:
        print(d)