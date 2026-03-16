import fitz
import pdfplumber
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "")

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
                    pages.append({
                        "page": i + 1,
                        "text": " ".join(page_text.split())
                    })

    except Exception as e:
        print("pdfplumber failed:", e)
        return []

    return pages


def extract_with_ocr(file_path):
    pages = []
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print("Failed to open PDF:", e)
        return []

    zoom = 3
    matrix = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        page_text = pytesseract.image_to_string(img)

        pages.append({
            "page": i + 1,
            "text": " ".join(page_text.split())
        })

    doc.close()
    return pages

def is_text_garbled(text):

    if not text:
        return True

    letters = sum(c.isalpha() for c in text)
    spaces = text.count(" ")

    if letters < len(text) * 0.2:
        return True

    if spaces < len(text) * 0.02:
        return True

    return False


def extract_text_from_pdf(file_path):

    print("Trying PyMuPDF extraction...")
    pages = extract_with_pymupdf(file_path)
    combined_text = " ".join(p["text"] for p in pages if p["text"])

    if combined_text and len(combined_text) > 100 and not is_text_garbled(combined_text):
        print("Extraction method used: PyMuPDF")
        return pages

    print("Text looks garbled. Trying pdfplumber...")
    pages = extract_with_pdfplumber(file_path)
    combined_text = " ".join(p["text"] for p in pages if p["text"])

    if combined_text and len(combined_text) > 100 and not is_text_garbled(combined_text):
        print("Extraction method used: pdfplumber")
        return pages

    print("Still bad. Switching to OCR...")

    if pages:
        print("Using previously extracted pages despite low confidence.")
        return pages

    pages = extract_with_ocr(file_path)

    if not pages:
        print("Warning: No text could be extracted from the PDF.")
        return []

    print("Extraction method used: OCR")

    return pages

if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    pages = extract_text_from_pdf(sample_file)

    full_text = " ".join(p["text"] for p in pages)
    print(full_text[:1000])