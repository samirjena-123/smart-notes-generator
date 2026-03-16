from docx import Document
import os

def extract_text_from_docx(file_path):

    pages = []
    text_parts = []

    try:
        doc = Document(file_path)
    except Exception as e:
        print("Failed to open DOCX:", e)
        return []

    # Extract paragraphs
    for para in doc.paragraphs:

        line = para.text.strip()

        if line:
            text_parts.append(line)

    # Extract tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    text_parts.append(cell_text)

    # Normalize whitespace
    full_text = " ".join(text_parts)
    full_text = " ".join(full_text.split())

    pages.append({
        "page": 1,
        "text": full_text
    })

    return pages


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.docx")

    pages = extract_text_from_docx(sample_file)

    full_text = " ".join(p["text"] for p in pages)
    print(full_text[:1000])