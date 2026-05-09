from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_Text(text):
    if not text or len(text.strip()) == 0:
        raise ValueError("empty text is received for the chunking")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)

    if len(chunks) == 0:
        raise ValueError("no chunks created from thr given text")

    return chunks
