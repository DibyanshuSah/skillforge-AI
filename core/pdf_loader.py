import os
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> str:
    """
    Load PDF from disk and extract text safely.
    This function MUST only accept a file path (not Streamlit uploaded_file).
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at path: {pdf_path}")

    reader = PdfReader(pdf_path)
    full_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)

    final_text = "\n".join(full_text)

    if not final_text.strip():
        raise ValueError("No readable text found in PDF")

    return final_text
