import os
import streamlit as st
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PDF_PATH = os.path.join(DATA_DIR, "uploaded.pdf")

# ---------------- CORE IMPORTS ----------------
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

# ---------------- UI ----------------
st.markdown("<h1>🔥 SkillForge AI</h1>", unsafe_allow_html=True)
st.caption("GenAI + RAG Adaptive Learning System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📄 Upload your study PDF")

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
    ["Explain", "Summary", "MCQ", "Interview"],
    index=0
)

# ---------------- PDF UPLOAD (CRITICAL FIX) ----------------
if uploaded_file is not None:
    try:
        # 🔥 THIS FIXES 403 ERROR
        with open(PDF_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.sidebar.success("PDF uploaded successfully")

        with st.spinner("Reading PDF..."):
            raw_text = load_pdf(PDF_PATH)

        with st.spinner("Chunking text..."):
            chunks = chunk_text(raw_text)

        with st.spinner("Creating vector store..."):
            vectorstore = create_or_load_vectorstore(chunks)

        st.session_state["vectorstore"] = vectorstore
        st.session_state["pdf_loaded"] = True

    except Exception as e:
        st.sidebar.error(f"PDF processing failed: {e}")

# ---------------- MAIN QA ----------------
st.subheader("💬 Ask from your document")

question = st.text_input(
    "Enter your question",
    placeholder="e.g. Explain this topic from basics"
)

if st.button("Generate Answer"):
    if not st.session_state.get("pdf_loaded"):
        st.warning("Please upload a PDF first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            relevant_chunks = get_relevant_chunks(
                st.session_state["vectorstore"],
                question
            )

            answer = generate_answer(
                context=relevant_chunks,
                user_query=question,
                difficulty=difficulty,
                mode=mode
            )

        st.markdown("### ✅ Answer")
        st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit, LangChain, FAISS, and Local/Cloud LLMs"
)
