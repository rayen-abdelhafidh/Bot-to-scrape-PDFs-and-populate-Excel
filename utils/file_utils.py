import fitz
import os

def is_scanned_pdf(filepath):
    with fitz.open(filepath) as doc:
        for page in doc:
            if page.get_text().strip():
                return False
    return True

def get_pdf_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.pdf')]
