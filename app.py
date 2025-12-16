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

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Remove extra top padding */
.block-container {
    padding-top: 1.5rem;
}

/* Center main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 25px;
}

/* Radio buttons as boxes */
div[role="radiogroup"] > label {
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px 16px;
    margin-right: 10px;
    background-color: #0b0f19;
    cursor: pointer;
}

/* Selected = RED */
div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #ef4444;
    color: white;
    border-color: #ef4444;
}

/* Reduce gap between sections */
h3 {
    margin-top: 10px;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🔥 SkillForge AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">GenAI + RAG Adaptive Learning System</div>', unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
left, right = st.columns([1.25, 1])

# ================= LEFT =================
with left:
    st.markdown("### 📘 Learning Content")

    difficulty = st.segmented_control(
    "Difficulty Level",
    options=["Easy", "Medium", "Hard"],
    default="Medium"
    )



    mode = st.segmented_control(
    "Learning Mode",
    options=["Explain", "Summary", "MCQ", "Interview"],
    default="Explain"
    )



    context_text = st.text_area(
        "Paste your PDF / Notes text",
        height=260,
        placeholder="Paste your study material here..."
    )

# ================= RIGHT =================
with right:
    st.markdown("### 💬 Ask Question")

    user_query = st.text_input(
        "Your Question",
        placeholder="e.g. Explain this topic from basics"
    )

    if st.button("🚀 Generate Answer", use_container_width=True):
        if not context_text.strip():
            st.error("Please paste learning content.")
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
                    difficulty,
                    mode
                )

            st.markdown("### 🤖 AI Response")
            st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FAISS and Local Phi-3 (GGUF)")
