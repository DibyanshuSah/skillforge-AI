import streamlit as st
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
/* Remove default padding */
.block-container {
    padding-top: 1.2rem;
}

/* Section titles */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* Selectable box buttons */
.select-box {
    display: inline-block;
    padding: 8px 16px;
    margin-right: 8px;
    margin-bottom: 6px;
    border-radius: 10px;
    border: 1px solid #333;
    cursor: pointer;
    background-color: #0f172a;
    color: white;
    font-weight: 500;
}

.select-box-selected {
    background-color: #f97316;
    border: 1px solid #f97316;
    color: black;
}

/* Textarea */
textarea {
    font-size: 15px !important;
}

/* Generate button */
button[kind="primary"] {
    background-color: #f97316 !important;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "mode" not in st.session_state:
    st.session_state.mode = "Explain"

# ---------------- LAYOUT ----------------
left, right = st.columns([1.2, 1])

# ================= LEFT =================
with left:
    st.markdown("## 📘 Learning Content")

    # ---- Difficulty Level (BOX STYLE) ----
    st.markdown('<div class="section-title">Difficulty Level</div>', unsafe_allow_html=True)
    diff_cols = st.columns(3)

    for i, level in enumerate(["Easy", "Medium", "Hard"]):
        with diff_cols[i]:
            selected = st.session_state.difficulty == level
            if st.button(
                level,
                key=f"diff_{level}",
                help=level,
            ):
                st.session_state.difficulty = level

    # ---- Learning Mode (BOX STYLE) ----
    st.markdown('<div class="section-title" style="margin-top:10px;">Learning Mode</div>', unsafe_allow_html=True)
    mode_cols = st.columns(4)

    for i, mode in enumerate(["Explain", "Summary", "MCQ", "Interview"]):
        with mode_cols[i]:
            if st.button(mode, key=f"mode_{mode}"):
                st.session_state.mode = mode

    # ---- PASTE TEXT ----
    st.markdown('<div class="section-title" style="margin-top:14px;">Paste your PDF / Notes text</div>', unsafe_allow_html=True)
    context_text = st.textarea(
        "",
        height=360,
        placeholder="Paste your study material here..."
    )

# ================= RIGHT =================
with right:
    st.markdown("## 💬 Ask Question")

    user_query = st.text_input(
        "Your Question",
        placeholder="e.g. summarize / explain from basics"
    )

    if st.button("Generate Answer", type="primary"):
        if not context_text.strip():
            st.error("❌ Please paste learning content first.")
        elif not user_query.strip():
            st.error("❌ Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = generate_answer(
                    context=context_text,
                    user_query=user_query,
                    difficulty=st.session_state.difficulty,
                    mode=st.session_state.mode
                )

            st.markdown("### 🤖 AI Response")
            st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using **Streamlit, LangChain, FAISS, and Hugging Face**",
    unsafe_allow_html=True
)
