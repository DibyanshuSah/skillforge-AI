import os
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> str:
    """
    Load PDF ONLY from disk path and extract text.
    HF-safe. No Streamlit object used here.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)

    final_text = "\n".join(pages_text)

    if not final_text.strip():
        raise ValueError("No readable text found in PDF")

    return final_text
