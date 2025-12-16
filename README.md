cat << 'EOF' > README.md
# 🔥 SkillForge AI

**SkillForge AI** is a **GenAI + RAG powered adaptive learning platform** that allows users to paste study material (PDF / notes) and ask intelligent questions with **difficulty control** and **learning modes**, powered by **local LLMs** and **vector search**.

---

## 🌐 Live Demo

Hugging Face Space:  
https://huggingface.co/spaces/rishusah/skillforge-ai

---

## ✨ Key Features

- 📘 Paste PDF / Notes text (no upload dependency)
- 🧠 Retrieval Augmented Generation (RAG) using FAISS
- 🎯 Difficulty Levels
  - Easy
  - Medium
  - Hard
- 🧪 Learning Modes
  - Explain
  - Summary
  - MCQs
  - Interview Q&A
- ⚡ Local LLM inference using GGUF models
- 🎨 Clean Streamlit UI
- 💻 Works locally and on Hugging Face Spaces

---

## 🧠 Architecture Overview

1. User pastes study content
2. Text is chunked into smaller segments
3. Embeddings are generated using Sentence Transformers
4. Embeddings stored in FAISS vector store
5. Relevant chunks retrieved using similarity search
6. Prompt dynamically constructed (difficulty + mode)
7. Local LLM generates final answer

---

## 🛠️ Tech Stack

- Frontend: Streamlit
- LLM: Local GGUF model (Phi-3)
- Inference Engine: llama-cpp-python
- Embeddings: Sentence-Transformers
- Vector Database: FAISS
- Deployment: Hugging Face Spaces (Docker)
- Language: Python

---

## 📁 Project Structure

skillforge-ai/
├── app.py
├── core/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── generator.py
├── data/
│   ├── uploads/
│   └── vectorstore/
├── models/
│   └── phi3.gguf
├── Dockerfile
├── requirements.txt
└── README.md

---

## ⚙️ Local Setup

Clone repository:
git clone https://github.com/DibyanshuSah/skillforge-AI.git
cd skillforge-AI

Create virtual environment:
python -m venv venv
source venv/bin/activate
# Windows: venv\\Scripts\\activate

Install dependencies:
pip install -r requirements.txt

Add local model:
models/phi3.gguf

Run app:
streamlit run app.py

---

## 📌 Notes

- Designed for offline usage with local LLMs
- No paid API keys required
- Same codebase runs locally and on Hugging Face
- Resume and interview ready GenAI project

---

## 👤 Author

Dibyanshu Sah  
GitHub: https://github.com/DibyanshuSah  
Hugging Face: https://huggingface.co/rishusah  

---

## ⭐ Support
If you find this project useful, consider giving it a ⭐ on GitHub.
If you find this project useful, consider giving it a ⭐ on GitHub.
EOF
