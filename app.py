import streamlit as st

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

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style="text-align:center;">🔥 SkillForge AI</h1>
    <p style="text-align:center;">
    GenAI + RAG Adaptive Learning System
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- LEFT RIGHT LAYOUT ----------------
left_col, right_col = st.columns([1.2, 1])

# ---------------- LEFT COLUMN (CONTENT INPUT) ----------------
with left_col:
    st.subheader("📄 Learning Content")

    raw_text = st.text_area(
        "Paste your PDF / Notes text here",
        height=420,
        placeholder="Paste extracted PDF text or notes here..."
    )

    difficulty = st.radio(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
        horizontal=True,
        index=1
    )

    mode = st.radio(
        "Learning Mode",
        ["Explain", "Summary", "MCQ", "Interview"],
        horizontal=True
    )

# ---------------- RIGHT COLUMN (QUESTION & OUTPUT) ----------------
with right_col:
    st.subheader("💬 Ask Question")

    question = st.text_input(
        "Your Question",
        placeholder="e.g. Explain this topic from basics"
    )

    generate = st.button("Generate Answer", type="primary")

    st.markdown("### 🤖 AI Response")

    if generate:
        if not raw_text.strip():
            st.warning("Please paste some learning content on the left.")
            st.stop()

        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Processing content..."):
            chunks = chunk_text(raw_text)
            vectorstore = create_or_load_vectorstore(chunks)
            context = get_relevant_chunks(vectorstore, question)

        with st.spinner("Generating answer..."):
            answer = generate_answer(
                context=context,
                user_query=question,
                difficulty=difficulty,
                mode=mode
            )

        st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit, FAISS, Transformers & Hugging Face"
)
