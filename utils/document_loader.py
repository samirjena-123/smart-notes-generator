import os

from extraction.pdf_parser import extract_text_from_pdf
from extraction.ppt_parser import extract_text_from_ppt
from extraction.docx_parser import extract_text_from_docx
from utils.text_cleaner import clean_text

MAX_FILE_SIZE_MB = 50


def load_document(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # file size check
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        print(f"Warning: File size {file_size_mb:.1f}MB exceeds {MAX_FILE_SIZE_MB}MB limit. Processing may be slow.")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".pdf":
        pages = extract_text_from_pdf(file_path)

    elif file_ext == ".pptx":
        pages = extract_text_from_ppt(file_path)

    elif file_ext == ".docx":
        pages = extract_text_from_docx(file_path)

    # Fix 2 — handle .ppt explicitly
    elif file_ext == ".ppt":
        print("Warning: .ppt files are not supported. Please convert to .pptx first.")
        return []

    # graceful return instead of crash
    else:
        print(f"Unsupported file type: {file_ext}. Supported: .pdf, .pptx, .docx")
        return []

    if not pages:
        print("Warning: No content extracted from document.")
        return []

    documents = []

    for item in pages:

        raw_text = item.get("text", "")

        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            continue

        page_number = item.get("page") or item.get("slide")
        if page_number is None:
            print(f"Warning: no page/slide key found in item, defaulting to 1")
            page_number = 1

        documents.append({
            "source": os.path.basename(file_path),
            "page": page_number,
            "text": cleaned_text,
        })

    return documents


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    docs = load_document(sample_file)

    for d in docs[:3]:
        print(d)