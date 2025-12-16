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

# ---------------- CONSTANTS ----------------
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

PDF_PATH = os.path.join(UPLOAD_DIR, "uploaded.pdf")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📄 Upload your study PDF")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"],
    accept_multiple_files=False
)

difficulty = st.sidebar.radio(
    "Difficulty level",
    ["Easy", "Medium", "Hard"],
    index=1
)

mode = st.sidebar.radio(
    "Learning Mode",
    ["Explain", "Summary", "MCQ", "Interview"]
)

# ---------------- PDF SAVE (🔥 FIXED PART) ----------------
if uploaded_file is not None:
    try:
        with open(PDF_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.sidebar.success("PDF uploaded successfully")

    except Exception as e:
        st.sidebar.error(f"PDF save failed: {e}")
        st.stop()

# ---------------- MAIN UI ----------------
st.markdown(
    """
    <h1>🔥 SkillForge AI</h1>
    <p>GenAI + RAG Adaptive Learning System</p>
    """,
    unsafe_allow_html=True
)

st.markdown("### 💬 Ask from your document")

query = st.text_input(
    "Enter your question",
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

    with st.spinner("Chunking document..."):
        chunks = chunk_text(text)

    with st.spinner("Creating / loading vector store..."):
        vectorstore = create_or_load_vectorstore(chunks)

    with st.spinner("Retrieving relevant context..."):
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
