from llama_cpp import Llama

# 🔥 Load model ONCE
llm = Llama(
    model_path="models/phi3.gguf",
    n_ctx=2048,
    n_threads=8,
    verbose=False
)

def generate_answer(context, user_query, difficulty, mode):
    prompt = f"""
You are a helpful AI tutor.

Difficulty: {difficulty}
Mode: {mode}

Use ONLY the context below to answer.

Context:
{context}

Question:
{user_query}

Answer clearly and simply.
"""

    response = llm.create_chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]
