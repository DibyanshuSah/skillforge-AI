def get_relevant_chunks(vectorstore, query, k=4):
    """
    Retrieves top-k relevant chunks for a given query.
    """

    if vectorstore is None:
        raise ValueError("Vectorstore not initialized")

    if not query or len(query.strip()) == 0:
        raise ValueError("Empty query received")

    # similarity search
    docs = vectorstore.similarity_search(query, k=k)

    if len(docs) == 0:
        raise ValueError("No relevant chunks found")

    # extract text content
    retrieved_text = "\n\n".join([doc.page_content for doc in docs])

    return retrieved_text
