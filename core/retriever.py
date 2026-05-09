def get_relevant_chunks(vectorstore, query, k=4):
    if vectorstore is None:
        raise ValueError("Vectorstore not initialized")
    if not query or len(query.strip()) == 0:
        raise ValueError("Empty query received")

    docs = vectorstore.similarity_search(query, k=k)
    if len(docs) == 0:
        raise ValueError("No relevant chunks found")
    retrieved_text = "\n\n".join([doc.page_content for doc in docs])
    return retrieved_text
