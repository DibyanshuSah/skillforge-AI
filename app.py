import os
from dotenv import load_dotenv
load_dotenv()

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

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    /* Sidebar width & background */
    section[data-testid="stSidebar"] {
        width: 390px !important;
    }

    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0f172a, #020617);
        color: white;
    }

    /* Primary button */
    button[kind="primary"] {
        background-color: #f97316 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
    }

    /* ✅ ONLY uploader BOX (not text) */
    div[data-testid="stFileUploader"] > section {
        border: 2px solid #f97316;
        border-radius: 16px;
        padding: 12px;
    }

    /* Reduce sidebar gaps */
    section[data-testid="stSidebar"] h3 {
        margin-top: 6px !important;
        margin-bottom: 4px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSegmentedControl"] {
        margin-top: 0px !important;
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] > div > div > div {
        gap: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- MAIN TITLE ----------------
st.markdown(
    """
    <h1 style="color:#f97316; margin-bottom:4px;">🔥 SkillForge AI</h1>
    <p style="color:gray; margin-top:0;">GenAI + RAG Adaptive Learning System</p>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# ======================================================
# 📄 SIDEBAR – PDF UPLOAD (TEXT OUTSIDE ORANGE BOX ✅)
# ======================================================
st.sidebar.markdown("### 📄 Upload your study PDF")

uploaded_file = st.sidebar.file_uploader(
    label="",
    type=["pdf"],
    label_visibility="collapsed"
)

# ---------------- PDF PROCESS ----------------
if uploaded_file and st.session_state.vectorstore is None:
    with st.sidebar.status("Processing document...", expanded=False):
        try:
            text = load_pdf(uploaded_file)
            chunks = chunk_text(text)
            st.session_state.vectorstore = create_or_load_vectorstore(chunks)
            st.sidebar.success("📘 Document loaded")
        except Exception as e:
            st.sidebar.error(f"❌ {e}")

elif st.session_state.vectorstore:
    st.sidebar.success("📘 Document loaded")

# ---------------- CONTROLS ----------------
difficulty = st.sidebar.segmented_control(
    "Difficulty level",
    options=["Easy", "Medium", "Hard"],
    default="Medium"
).lower()

mode = st.sidebar.segmented_control(
    "Learning Mode",
    options=["Explain", "Summary", "MCQ", "Interview"],
    default="Explain"
).lower()

with st.sidebar.expander("⚙️ Advanced options"):
    st.checkbox("Strictly use document content", value=True, disabled=True)
    st.checkbox("Show answer sources", value=True, disabled=True)

# ---------------- MAIN UI ----------------
st.markdown("## 💬 Ask from your document")

user_query = st.text_input(
    "Enter your question",
    placeholder="e.g. Explain this topic from basics"
)

can_generate = st.session_state.vectorstore is not None and user_query.strip()

if st.button("Generate Answer", type="primary", disabled=not can_generate):
    with st.spinner("🤖 Generating answer..."):
        try:
            context = get_relevant_chunks(
                st.session_state.vectorstore,
                user_query
            )

            answer = generate_answer(
                context=context,
                user_query=user_query,
                difficulty=difficulty,
                mode=mode
            )

            st.markdown("### 🧠 Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with ❤️ using LangChain, FAISS, Streamlit, and Local/Cloud LLMs")
