import fitz
import pdfplumber
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"D:\Ocr\tesseract.exe"

def extract_with_pymupdf(file_path):
    text = ""
    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text("text")

    doc.close()
    return text


def extract_with_pdfplumber(file_path):
    import pdfplumber
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print("pdfplumber failed:", e)
        return ""

    return text


def extract_with_ocr(file_path):
    text = ""
    doc = fitz.open(file_path)

    zoom = 3  # increases resolution (3x ≈ 300 DPI)
    matrix = fitz.Matrix(zoom, zoom)

    for page in doc:
        pix = page.get_pixmap(matrix=matrix)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        page_text = pytesseract.image_to_string(img)
        text += page_text + "\n"

    doc.close()
    return text


def is_text_garbled(text):
    letters = sum(c.isalpha() for c in text)
    spaces = text.count(" ")

    if letters < len(text) * 0.4:
        return True
    if spaces < len(text) * 0.05:
        return True

    return False


def extract_text_from_pdf(file_path):

    print("Trying PyMuPDF extraction...")
    text = extract_with_pymupdf(file_path)

    if text and not is_text_garbled(text):
        print("Extraction method used: PyMuPDF")
        return text

    print("Text looks garbled. Trying pdfplumber...")
    text = extract_with_pdfplumber(file_path)

    if text and not is_text_garbled(text):
        print("Extraction method used: pdfplumber")
        return text

    print("Still bad. Switching to OCR...")
    text = extract_with_ocr(file_path)

    print("Extraction method used: OCR")

    return text

if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    text = extract_text_from_pdf(sample_file)

    print("\n----- Extracted Text -----\n")
    print(text[:1000])