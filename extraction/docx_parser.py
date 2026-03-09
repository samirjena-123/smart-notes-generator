from docx import Document
import os


def extract_text_from_docx(file_path):

    doc = Document(file_path)
    pages = []

    text = ""

    for para in doc.paragraphs:
        line = para.text.strip()

        if line:
            text += line + "\n"

    pages.append({
        "page": 1,
        "text": text
    })

    return pages


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    pages = extract_text_from_docx(sample_file)

    full_text = " ".join(p["text"] for p in pages)
    print(full_text[:1000])