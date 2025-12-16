import os
import streamlit as st
import requests

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
st.markdown(
    """
    <h1>🔥 SkillForge AI</h1>
    <p>GenAI + RAG Adaptive Learning System</p>
    """,
    unsafe_allow_html=True
)

st.info(
    "⚠️ PDF upload disabled on HF Free tier due to proxy limits. "
    "Use **PDF URL** or **Paste Text** (production-safe approach)."
)

# ---------------- INPUT MODE ----------------
mode_input = st.radio(
    "Choose input method",
    ["Paste Text", "PDF URL"]
)

raw_text = ""

if mode_input == "Paste Text":
    raw_text = st.text_area(
        "Paste PDF text here",
        height=300,
        placeholder="Paste extracted PDF text here..."
    )

else:
    pdf_url = st.text_input(
        "Enter direct PDF URL (raw GitHub / Drive / HF Dataset)",
        placeholder="https://example.com/file.pdf"
    )

    if st.button("Fetch PDF"):
        if not pdf_url.strip():
            st.error("Please enter a PDF URL")
        else:
            try:
                resp = requests.get(pdf_url, timeout=20)
                resp.raise_for_status()

                with open("temp.pdf", "wb") as f:
                    f.write(resp.content)

                from core.pdf_loader import load_pdf
                raw_text = load_pdf("temp.pdf")
                st.success("PDF fetched & read successfully")

            except Exception as e:
                st.error(f"Failed to fetch PDF: {e}")

# ---------------- SETTINGS ----------------
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
learn_mode = st.selectbox("Learning Mode", ["Explain", "Summary", "MCQ", "Interview"])

question = st.text_input(
    "Ask a question",
    placeholder="e.g. Explain this topic from basics"
)

# ---------------- GENERATE ----------------
if st.button("Generate Answer"):
    if not raw_text.strip():
        st.error("No content provided")
        st.stop()

    if not question.strip():
        st.error("Please enter a question")
        st.stop()

    with st.spinner("Chunking text..."):
        chunks = chunk_text(raw_text)

    with st.spinner("Creating vector store..."):
        vectorstore = create_or_load_vectorstore(chunks)

    with st.spinner("Retrieving relevant context..."):
        context = get_relevant_chunks(vectorstore, question)

    with st.spinner("Generating answer..."):
        answer = generate_answer(
            context=context,
            user_query=question,
            difficulty=difficulty,
            mode=learn_mode
        )

    st.markdown("### ✅ Answer")
    st.write(answer)
