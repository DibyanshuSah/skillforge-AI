import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTORSTORE_DIR = "data/vectorstore"


def get_embedding_model():
    """
    Lightweight embedding model (CPU friendly, deploy safe)
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_or_load_vectorstore(chunks):
    """
    Creates FAISS vector store if not exists,
    otherwise loads from disk.
    """

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    embeddings = get_embedding_model()

    index_path = os.path.join(VECTORSTORE_DIR, "faiss_index")

    # Load existing index (important for Streamlit reruns)
    if os.path.exists(index_path):
        vectorstore = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore

    # Create new index
    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    # Save to disk (deploy-safe)
    vectorstore.save_local(index_path)

    return vectorstore
