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

# ---------------- SESSION STATE ----------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "mode" not in st.session_state:
    st.session_state.mode = "Explain"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.block-btn button {
    border-radius: 10px;
    padding: 10px 18px;
    margin-right: 10px;
    margin-bottom: 10px;
    border: 1px solid #333;
    background-color: #111;
    color: white;
}
.block-btn button:hover {
    border-color: #f97316;
    color: #f97316;
}
.selected-btn {
    background-color: #f97316 !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI LAYOUT ----------------
left, right = st.columns([1.2, 1])

# ================= LEFT SIDE =================
with left:
    st.markdown("## 📘 Learning Content")

    # -------- Difficulty Level --------
    st.markdown("### Difficulty Level")
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Easy", key="easy"):
            st.session_state.difficulty = "Easy"
    with c2:
        if st.button("Medium", key="medium"):
            st.session_state.difficulty = "Medium"
    with c3:
        if st.button("Hard", key="hard"):
            st.session_state.difficulty = "Hard"

    # -------- Learning Mode --------
    st.markdown("### Learning Mode")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        if st.button("Explain"):
            st.session_state.mode = "Explain"
    with m2:
        if st.button("Summary"):
            st.session_state.mode = "Summary"
    with m3:
        if st.button("MCQ"):
            st.session_state.mode = "MCQ"
    with m4:
        if st.button("Interview"):
            st.session_state.mode = "Interview"

    # -------- Context Text --------
    st.markdown("### Paste your PDF / Notes text")
    context_text = st.text_area(
        label="",
        height=320,
        placeholder="Paste your study material here..."
    )

# ================= RIGHT SIDE =================
with right:
    st.markdown("## 💬 Ask Question")

    user_query = st.text_input(
        "Your Question",
        placeholder="e.g. Explain this topic from basics"
    )

    generate = st.button("🚀 Generate Answer")

    if generate:
        if not context_text.strip():
            st.error("Please paste some learning content first.")
        elif not user_query.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                chunks = chunk_text(context_text)
                vectorstore = create_or_load_vectorstore(chunks)
                relevant_context = get_relevant_chunks(
                    vectorstore,
                    user_query
                )

                answer = generate_answer(
                    relevant_context,
                    user_query,
                    st.session_state.difficulty,
                    st.session_state.mode
                )

            st.markdown("## 🤖 AI Response")
            st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit, FAISS and Local Phi-3 (GGUF)"
)
