import os
import streamlit as st
from dotenv import load_dotenv

from core.pdf_loader import load_pdf
from core.chunker import chunk_text
from core.embeddings import create_or_load_vectorstore
from core.retriever import get_relevant_chunks
from core.generator import generate_answer

# ---------------- ENV ----------------
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🔥",
    layout="wide"
)

# ---------------- PATHS (HF SAFE) ----------------
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 📄 Upload your study PDF")

    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["pdf"]
    )

    st.markdown("### 🎯 Difficulty level")
    difficulty = st.radio(
        "",
        ["Easy", "Medium", "Hard"],
        horizontal=True,
        index=1
    )

    st.markdown("### 🧠 Learning Mode")
    mode = st.radio(
        "",
        ["Explain", "Summary", "MCQ", "Interview"],
        horizontal=True
    )

# ---------------- MAIN UI ----------------
st.markdown(
    """
    <h1 style='color:#f97316;'>🔥 SkillForge AI</h1>
    <p>GenAI + RAG Adaptive Learning System</p>
    """,
    unsafe_allow_html=True
)

query = st.text_input(
    "Ask from your document",
    placeholder="e.g. Explain this topic from basics"
)

# ---------------- PDF PROCESSING ----------------
pdf_path = None
vectorstore = None

if uploaded_file:
    pdf_path = os.path.join(DATA_DIR, uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"PDF uploaded successfully")

    with st.spinner("📚 Reading PDF..."):
        text = load_pdf(pdf_path)

    with st.spinner("✂️ Chunking content..."):
        chunks = chunk_text(text)

    with st.spinner("🧠 Creating embeddings..."):
        vectorstore = create_or_load_vectorstore(chunks)

# ---------------- GENERATE ANSWER ----------------
if st.button("Generate Answer", type="primary"):
    if not uploaded_file:
        st.warning("Please upload a PDF first")
    elif not query.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("🤖 Thinking..."):
            relevant_chunks = get_relevant_chunks(vectorstore, query)
            answer = generate_answer(
                context=relevant_chunks,
                user_query=query,
                difficulty=difficulty,
                mode=mode
            )

        st.markdown("### ✅ Answer")
        st.write(answer)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <small>Built with ❤️ using LangChain, FAISS, Streamlit & Hugging Face</small>
    """,
    unsafe_allow_html=True
)
