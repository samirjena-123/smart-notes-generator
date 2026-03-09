from pptx import Presentation
import os


def extract_text_from_ppt(file_path):

    prs = Presentation(file_path)
    slides = []

    for i, slide in enumerate(prs.slides):

        slide_text = ""

        for shape in slide.shapes:

            # Text frames
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = paragraph.text.strip()
                    if line:
                        slide_text += line + "\n"

            # Tables
            if shape.has_table:
                table = shape.table

                for row in table.rows:
                    for cell in row.cells:
                        cell_text = cell.text.strip()
                        if cell_text:
                            slide_text += cell_text + "\n"

        slides.append({
            "slide": i + 1,
            "text": slide_text
        })

    return slides


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pptx")

    slides = extract_text_from_ppt(sample_file)

    full_text = " ".join(s["text"] for s in slides)
    print(full_text[:1000])