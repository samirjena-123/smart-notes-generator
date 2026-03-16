from pptx import Presentation
import os

def extract_text_from_ppt(file_path):

    slides = []
    text_parts = []

    try:
        prs = Presentation(file_path)
    except Exception as e:
        print("Failed to open PPT/PPTX:", e)
        return []

    for i, slide in enumerate(prs.slides):

        slide_parts = []

        for shape in slide.shapes:

            # Extract text from text frames
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = paragraph.text.strip()

                    if line:
                        slide_parts.append(line)

            # Extract table text
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:

                        cell_text = cell.text.strip()

                        if cell_text:
                            slide_parts.append(cell_text)

        # Normalize whitespace
        slide_text = " ".join(slide_parts)
        slide_text = " ".join(slide_text.split())

        if slide_text:
            slides.append({
                "slide": i + 1,
                "text": slide_text
            })

    return slides


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.ppt")

    slides = extract_text_from_ppt(sample_file)

    full_text = " ".join(s["text"] for s in slides)
    print(full_text[:1000])