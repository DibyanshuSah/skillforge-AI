from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):
    """
    Splits large text into smaller overlapping chunks for RAG.
    """

    if not text or len(text.strip()) == 0:
        raise ValueError("Empty text received for chunking")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(text)

    if len(chunks) == 0:
        raise ValueError("No chunks created from text")

    return chunks
