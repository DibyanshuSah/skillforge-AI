import os
import streamlit as st

from core.pdf_loader import load_pdf
from core.chunker import chunk_text
from core.embeddings import create_or_load_vectorstore
from core.retriever import get_relevant_chunks
from core.generator import generate_answer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🔥",
    layout="wide"
)

# ---------------- PATHS ----------------
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

PDF_PATH = os.path.join(UPLOAD_DIR, "uploaded.pdf")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📄 Upload your study PDF")

with st.sidebar.form("pdf_upload_form", clear_on_submit=False):

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=False
    )

    upload_btn = st.form_submit_button("Upload PDF")

    if upload_btn and uploaded_file is not None:
        try:
            with open(PDF_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state["pdf_uploaded"] = True
            st.success("PDF uploaded successfully")
        except Exception as e:
            st.error(f"Upload failed: {e}")
            st.stop()

difficulty = st.sidebar.radio(
    "Difficulty",
    ["Easy", "Medium", "Hard"],
    index=1
)

mode = st.sidebar.radio(
    "Mode",
    ["Explain", "Summary", "MCQ", "Interview"]
)

# ---------------- MAIN UI ----------------
st.markdown(
    """
    <h1>🔥 SkillForge AI</h1>
    <p>GenAI + RAG Adaptive Learning System</p>
    """,
    unsafe_allow_html=True
)

query = st.text_input(
    "Ask a question from your document",
    placeholder="e.g. Explain this topic from basics"
)

# ---------------- GENERATE ANSWER ----------------
if st.button("Generate Answer"):

    if not os.path.exists(PDF_PATH):
        st.error("Please upload a PDF first.")
        st.stop()

    if not query.strip():
        st.error("Please enter a question.")
        st.stop()

    with st.spinner("Reading PDF..."):
        text = load_pdf(PDF_PATH)

    with st.spinner("Chunking text..."):
        chunks = chunk_text(text)

    with st.spinner("Creating / loading vector store..."):
        vectorstore = create_or_load_vectorstore(chunks)

    with st.spinner("Retrieving relevant content..."):
        context = get_relevant_chunks(vectorstore, query)

    with st.spinner("Generating answer..."):
        answer = generate_answer(
            context=context,
            user_query=query,
            difficulty=difficulty,
            mode=mode
        )

    st.markdown("### ✅ Answer")
    st.write(answer)
