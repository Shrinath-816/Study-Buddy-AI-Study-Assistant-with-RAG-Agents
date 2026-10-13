"""
STEP 08  -  Text Splitters: cutting documents into small chunks
===============================================================
📖 Read first: learning_notes/08_text_splitters.md  (simple explanation with diagrams)

WHY SPLIT?
    1. When a student asks a question, only a small PART of the notes is relevant.
       Sending only that part gives better, more focused answers.
    2. LLM calls cost tokens. Sending whole books every time is slow and expensive.
    3. Search works better on small, focused pieces of text.

HOW: RecursiveCharacterTextSplitter (the most commonly used splitter)
    It tries to split at natural boundaries, in this order:
        paragraphs ("\\n\\n")  ->  lines ("\\n")  ->  sentences/words (" ")  ->  characters
    so chunks usually end at a sensible place instead of mid-word.

    chunk_size    = maximum characters per chunk
    chunk_overlap = characters repeated between neighbouring chunks, so that
                    an idea cut at the border is not lost.

    Each chunk is still a Document, and it KEEPS the metadata of its parent
    (so we still know which file it came from).

Run this file:   python step08_text_splitters.py
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from step07_document_loaders import load_notes


def split_documents(documents: list[Document], chunk_size: int = 800, chunk_overlap: int = 100) -> list[Document]:
    """Split a list of Documents into smaller chunk Documents."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,  # adds "start_index" to metadata: where the chunk begins in the original
    )
    return splitter.split_documents(documents)


def small_example():
    """Split a short text with tiny chunks so you can SEE the overlap."""
    text = ("Mitochondria are the powerhouse of the cell. They produce energy. "
            "Chloroplasts are found in plant cells. They perform photosynthesis.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=60, chunk_overlap=15)
    chunks = splitter.split_text(text)  # split_text works on a plain string

    for number, chunk in enumerate(chunks, start=1):
        print(f"  Chunk {number}: '{chunk}'")


if __name__ == "__main__":
    print("=== 1. A tiny example (chunk_size=60, overlap=15) ===")
    small_example()

    print("\n=== 2. Splitting our real notes ===")
    documents = load_notes()
    chunks = split_documents(documents)
    print(f"{len(documents)} documents  ->  {len(chunks)} chunks\n")

    for chunk in chunks[:3]:  # show the first 3 chunks
        print("Metadata:", chunk.metadata)
        print("Text    :", chunk.page_content[:200].replace("\n", " "), "...\n")
