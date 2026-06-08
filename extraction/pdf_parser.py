import fitz
import pdfplumber
import re
import os


def extract_with_pymupdf(file_path):
    pages = []
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print("Failed to open PDF:", e)
        return []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text and text.strip():
            text = re.sub(r'(\d)\s*\.\s*(\d)', r'\1.\2', text)
            pages.append({
            "page": i + 1,
            "text": " ".join(text.split())
            })

    doc.close()
    return pages


def extract_with_pdfplumber(file_path):
    pages = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):

                page_text = page.extract_text()

                if page_text:
                    page_text = re.sub(
                        r'(\d)\s*\.\s*(\d)',
                        r'\1.\2',
                        page_text
                    )

                    pages.append({
                        "page": i + 1,
                        "text": " ".join(page_text.split())
                    })
                
    except Exception as e:
        print("pdfplumber failed:", e)
        return []

    return pages



def is_text_garbled(text):
    if not text or len(text.strip()) < 30:
        return True

    letters = sum(c.isalpha() for c in text)
    spaces = text.count(" ")

    if letters < len(text) * 0.2:
        return True
    if spaces < len(text) * 0.02:
        return True

    return False


def extract_text_from_pdf(file_path):

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    print("Trying PyMuPDF extraction...")
    pages = extract_with_pymupdf(file_path)
    combined_text = " ".join(p["text"] for p in pages if p["text"])

    if combined_text and not is_text_garbled(combined_text):
        print("Extraction method used: PyMuPDF")
        return pages

    print("Text looks garbled. Trying pdfplumber...")
    pages = extract_with_pdfplumber(file_path)
    combined_text = " ".join(p["text"] for p in pages if p["text"])

    if combined_text and not is_text_garbled(combined_text):
        print("Extraction method used: pdfplumber")
        return pages

    print("Warning: No readable text found in PDF.")
    return []

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    pages = extract_text_from_pdf(sample_file)

    # Show page 10 text specifically
    for p in pages:
        if p["page"] == 10:
            print(f"Page 10 raw text:")
            print(repr(p["text"]))  # repr shows hidden characters