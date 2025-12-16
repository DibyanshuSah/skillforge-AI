import os
from pypdf import PdfReader

UPLOAD_DIR = "data/uploads"


def save_uploaded_pdf(uploaded_file):
    """
    Saves uploaded PDF to disk safely.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from PDF file.
    """
    reader = PdfReader(pdf_path)
    full_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)

    return "\n".join(full_text)


def load_pdf(uploaded_file):
    """
    Main function used by app.py
    """
    if uploaded_file is None:
        raise ValueError("No PDF uploaded")

    # Safety check (size limit ~15MB)
    if uploaded_file.size > 15 * 1024 * 1024:
        raise ValueError("PDF too large. Upload file under 15MB.")

    pdf_path = save_uploaded_pdf(uploaded_file)
    text = extract_text_from_pdf(pdf_path)

    if len(text.strip()) == 0:
        raise ValueError("Could not extract text from PDF")

    return text
