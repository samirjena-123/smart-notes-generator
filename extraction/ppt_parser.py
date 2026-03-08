from pptx import Presentation
import os

def extract_text_from_ppt(file_path):
    prs = Presentation(file_path)
    text = ""

    for slide in prs.slides:
        for shape in slide.shapes:

            # Text frames
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = paragraph.text.strip()
                    if line:
                        text += line + "\n"

            # Tables
            if shape.has_table:
                table = shape.table

                for row in table.rows:
                    for cell in row.cells:
                        cell_text = cell.text.strip()
                        if cell_text:
                            text += cell_text + "\n"

    return text

if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pptx")
    text = extract_text_from_ppt(sample_file)

    print("\n----- Extracted Text -----\n")
    print(text[:1000])