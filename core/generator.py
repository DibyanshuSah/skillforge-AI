import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# ---------------- MODEL CONFIG ----------------
REPO_ID = "lmstudio-community/TinyLlama-1.1B-Chat-GGUF"
MODEL_FILE = "tinyllama-1.1b-chat.Q4_K_M.gguf"

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# ---------------- DOWNLOAD MODEL AT RUNTIME ----------------
model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=MODEL_FILE,
    local_dir=MODELS_DIR,
    local_dir_use_symlinks=False
)

# ---------------- LOAD LLM ----------------
llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=4,
    n_batch=256,
    verbose=False
)

# ---------------- PROMPT LOADER ----------------
def load_prompt(difficulty: str):
    prompt_map = {
        "Easy": "prompts/easy.txt",
        "Medium": "prompts/medium.txt",
        "Hard": "prompts/hard.txt",
    }

    path = prompt_map.get(difficulty, "prompts/medium.txt")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return "You are a helpful AI tutor."

# ---------------- MAIN GENERATION ----------------
def generate_answer(context: str, user_query: str, difficulty: str, mode: str):

    system_prompt = load_prompt(difficulty)

    final_prompt = f"""
{system_prompt}

Mode: {mode}

Context:
{context}

Question:
{user_query}

Answer:
"""

    response = llm(
        final_prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        stop=["</s>"]
    )

    return response["choices"][0]["text"].strip()
