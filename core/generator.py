from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    device_map="auto"
)

def load_prompt(difficulty: str):
    path = f"prompts/{difficulty.lower()}.txt"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "You are a helpful AI tutor."

def generate_answer(context: str, user_query: str, difficulty: str, mode: str):

    system_prompt = load_prompt(difficulty)

    prompt = f"""
{system_prompt}

Mode: {mode}

Context:
{context}

Question:
{user_query}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
